import os, sys,inspect
from gevent import monkey

monkey.patch_all()
from gevent.pool import Pool
import subprocess
import numpy as np
import re
import time
from threading import Thread
import uuid

#from pathlib import Path
from tractcrush.ux import MsgUser
import nibabel as nib
from shutil import copyfile
import multiprocessing
import csv
import warnings
from collections import defaultdict

              
class Visit:
   
        
    def __init__(self,path,rebuild,voi,recrush,fixmissing):
       
        self.VisitId=os.path.basename(path)
        self.path=path
        self.rebuild=rebuild
        self.voi=voi        
        self.recrush=recrush
        self.fixmissing=fixmissing
        self.data = defaultdict(list)#{}
        self.PatientId=os.path.split(os.path.dirname(self.path))[1]
        reconTest= "%s/Freesurfer/mri/wmparc.mgz" % (path)
        
        if os.path.isfile(reconTest):
            self.ReconComplete=True            
        else:
            self.ReconComplete=False

        measurementTest = "%s/Tractography/crush/tracts.txt" % (path)
        #print(measurementTest)
        if os.path.isfile(measurementTest):
            self.MeasurementComplete=True    
        else: 
            self.MeasurementComplete=False


        self.Segments = []#{}

        i=1
        segmentMap="%s/%s" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),"segmentMap.txt")
        with open(segmentMap) as fin:
            reader=csv.reader(fin, skipinitialspace=True, quotechar="'")
            p = re.compile('^ *#')   # if not commented          
            for row in reader:
                #print("%s,%s" %(i,row))
                if(not p.match(row[0])): 
                    self.Segments.append({'roi':row[0],'roiname':row[1],'asymmetry':row[2]})
                    #self.Segments[i]={} 
                    #self.Segments[i]['roi']=row[0]
                    #self.Segments[i]['roiname']=row[1]
                    #self.Segments[i]['asymmetry']=row[2]
                i=i+1
                    #self.Segments[row[0]]=row[1:] 
        # segmentMap="%s/%s" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),"segmentMap.txt")
        # with open(segmentMap) as fin:
        #     reader=csv.reader(fin, skipinitialspace=True, quotechar="'")
        #     p = re.compile('^ *#')   # if not commented          
        #     for row in reader:
        #         if(not p.match(row[0])):                    
        #             self.Segments[row[0]]=row[1:]                        
                            
        #print(self.Segments)
    def Render(self):
        #Lets Render as needed
        MsgUser.message("Rendering %s" % self.path)
        

        self.mgz2nifti()
        self.eddy_correct()
        self.hardi_mat()
        self.odf_recon()
        self.odf_tracker()
        self.flirt()
        self.tract_transform()
        self.dti_recon()
        self.dti_tracker()
        
    def Measure(self):
    
        self.track_vis()

    def GetMeasurements(self):

        Measurements={}

        self.data[self.PatientId]={}
        self.data[self.PatientId][self.VisitId]={}

        if os.path.isfile("%s/Tractography/crush/tracts.txt" %(self.path)):
            with open("%s/Tractography/crush/tracts.txt" %(self.path)) as fMeasure:
                for line in fMeasure:
                    nvp=line.split("=")   
                    self.data[self.PatientId][self.VisitId][nvp[0]]=nvp[1].strip()
                    Measurements[nvp[0]]=nvp[1].strip()
        
        ## Add derived measures here
        #print("Deriving Asymmetry Indexes")
        for s in self.Segments:  
            roi=s['roi']                             
            asymmetry=s['asymmetry']
            if asymmetry:
                for p in self.data:
                    for v in self.data[p]: 
                        asymMeasuresToAdd = {}
                        for m in self.data[p][v]:
                            #For all measures                                                                                      
                            searchEx="%s-%s" %(roi,r'(\d+)')
                            roiGrp = re.search(searchEx, m)
                            if roiGrp:
                                ma=m.replace(roi,asymmetry)
                                if ma in self.data[p][v] and float(self.data[p][v][ma]) != 0:
                                    asymIdx=float(self.data[p][v][m]) / float(self.data[p][v][ma])
                                else:
                                    asymIdx=0
                                #self.data[self.PatientId][self.VisitId][ma]=asymIdx
                                
                                asymMeasuresToAdd["%s-asymidx" %(ma)]=asymIdx
                                #print("%s [%s] has aymmetry with %s [%s].  ASYM IDX=[%s]" %(m,self.data[p][v][m],ma,self.data[p][v][ma],asymIdx))
                                #print("%s is %s" %(ma,asymIdx))
                        for ma in asymMeasuresToAdd:                                                                
                            #print("XX-%s" %(ma))
                            self.data[p][v][ma] = str(asymMeasuresToAdd[ma])

                
        ## End of derived measures
        
        return Measurements
        #Print report
        for p in self.data:            
            for v in self.data[p]:
                row=[]
                row.append(p)
                row.append(v)
                for m in voi_interests:
                    if m in self.data[p][v]:
                        row.append(self.data[p][v][m])
                        if "%s-asymidx" %(m) in self.data[p][v]:
                            row.append(self.data[p][v]["%s-asymidx" %(m)])
                    else:
                        row.append("")
            #print(",".join(row))   
        

    def Report2(self):
        #MsgUser.bold("Reporting values of interest")

        if os.path.isfile("%s" %(self.voi)):
            #Determine my interests
            with open(self.voi) as f:
                voi_interests = f.readlines()
                voi_interests = [x.strip() for x in voi_interests] #Remove Whitespace
            #Get everything
            self.data[self.PatientId]={}
            self.data[self.PatientId][self.VisitId]={}

            if os.path.isfile("%s/Tractography/crush/tracts.txt" %(self.path)):
                with open("%s/Tractography/crush/tracts.txt" %(self.path)) as fMeasure:
                    for line in fMeasure:
                        nvp=line.split("=")   
                        self.data[self.PatientId][self.VisitId][nvp[0]]=nvp[1].strip()
            
            ## Add derived measures here
            #print("Deriving Asymmetry Indexes")
            for s in self.Segments:  
                roi=s['roi']                             
                asymmetry=s['asymmetry']
                if asymmetry:
                    for p in self.data:
                        for v in self.data[p]: 
                            asymMeasuresToAdd = {}
                            for m in self.data[p][v]:
                                #For all measures                                                                                      
                                searchEx="%s-%s" %(roi,r'(\d+)')
                                roiGrp = re.search(searchEx, m)
                                if roiGrp:
                                    ma=m.replace(roi,asymmetry)
                                    if ma in self.data[p][v] and float(self.data[p][v][ma]) != 0:
                                        asymIdx=float(self.data[p][v][m]) / float(self.data[p][v][ma])
                                    else:
                                        asymIdx=0
                                    #self.data[self.PatientId][self.VisitId][ma]=asymIdx
                                    
                                    asymMeasuresToAdd["%s-asymidx" %(ma)]=asymIdx
                                    #print("%s [%s] has aymmetry with %s [%s].  ASYM IDX=[%s]" %(m,self.data[p][v][m],ma,self.data[p][v][ma],asymIdx))
                                    #print("%s is %s" %(ma,asymIdx))
                            for ma in asymMeasuresToAdd:                                                                
                                #print("XX-%s" %(ma))
                                self.data[p][v][ma] = str(asymMeasuresToAdd[ma])

                   
            ## End of derived measures

            #Print report
            for p in self.data:
                for v in self.data[p]:
                    row=[]
                    row.append(p)
                    row.append(v)
                    for m in voi_interests:
                        if m in self.data[p][v]:
                            row.append(self.data[p][v][m])
                            if "%s-asymidx" %(m) in self.data[p][v]:
                                row.append(self.data[p][v]["%s-asymidx" %(m)])
                        else:
                            row.append("")
            print(",".join(row))                        
       
    def Report(self):
        #MsgUser.bold("Reporting values of interest")

        if os.path.isfile("%s" %(self.voi)):
            #Determine my interests
            with open(self.voi) as f:
                content = f.readlines()
                content = [x.strip() for x in content] #Remove Whitespace
            #Read the measures that have been pre-derived   
            measures={}
            
            measures["PatientVisit"]=self.path           
            
            if os.path.isfile("%s/Tractography/crush/tracts.txt" %(self.path)):
                with open("%s/Tractography/crush/tracts.txt" %(self.path)) as fMeasure:
                    for line in fMeasure:
                        nvp=line.split("=")                        
                        measures[nvp[0]]=nvp[1]



                
                row=[]
                row.append(os.path.split(os.path.dirname(self.path))[1])
                row.append(self.VisitId)

                #self.data['key'].append
                
                for cell in content:
                    if cell in measures:
                        row.append(measures[cell].strip())
                        
                 #       self.data[(os.path.split(os.path.dirname(self.path))[1])][self.VisitId][cell]=measures[cell].strip()
                    else:
                        row.append("")                              
                print(",".join(row))
                
                    
            
        
    def mgz2nifti(self):  
        MsgUser.bold("mgz2nifti")
        if self.rebuild!=True and os.path.isfile("%s/Freesurfer/mri/brainmask.nii" % (self.path)):
            self.NiftiComplete=True
            MsgUser.skipped("All Nifti files exist")
        else:
            MsgUser.warning("\tNifti Incomplete, rendering nii files...")
                 
            mgzFiles=['aseg','aparc+aseg', 'aparc.a2009s+aseg', 'lh.ribbon', 'rh.ribbon', 'nu', 'orig', 'ribbon', 'wm.asegedit', 'wm', 'wm.seg', 'brain', 'brainmask']
       
            for mgz in mgzFiles:
                if os.path.isfile("%s/Freesurfer/mri/%s.nii" % (self.path,mgz)) :
                    MsgUser.skipped("\t%s.nii exists" % (mgz))
                else:
                
                    MsgUser.message("Create or replace %s.nii" % (mgz))
                    subprocess.call(['mri_convert','-rt','nearest','-nc','-ns','1',"%s/Freesurfer/mri/%s.mgz" %(self.path,mgz),"%s/Freesurfer/mri/%s.nii" % (self.path,mgz)])

    def eddy_correct(self):
        MsgUser.bold("eddy_correct")
        #eddy_correct ~/HealthyTractography/%s/%s/DTI35.nii ~/HealthyTractography/%s/%s/DTI35_eddy.nii 0
        
        if self.rebuild!=True  and os.path.isfile("%s/Tractography/DTI35_eddy.nii.gz" %(self.path)):
            MsgUser.skipped("eddy_correct output exists")
        else:
            
            cmdArray=["eddy_correct","%s/Tractography/DTI35.nii" % (self.path),"%s/Tractography/DTI35_eddy.nii.gz" % (self.path),"0"]
            print (cmdArray)
            subprocess.call(cmdArray)
            
            MsgUser.ok("eddy_correct Completed")

            
        
    def hardi_mat(self):
        MsgUser.bold("hardi_mat")
        if self.rebuild!=True and os.path.isfile("%s/Tractography/temp_mat.dat" %(self.path)):
            MsgUser.skipped("hardi_mat output exists")
        else:
            defaultGradientMatrix ="%s/%s" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),"gradientMatrix.txt")
            
            cmdArray=["hardi_mat",defaultGradientMatrix,"%s/Tractography/temp_mat.dat" % (self.path), "-ref","%s/Tractography/DTI35_eddy.nii.gz" % (self.path),"-oc"]
            print(cmdArray)
            subprocess.call(cmdArray)
            
            MsgUser.ok("HARDIReconstruction Completed")

            
    def odf_recon(self):
        MsgUser.bold("odf_recon")
        #output: DTI35_Recon_max.nii.gz
        if self.rebuild!=True  and os.path.isfile("%s/Tractography/DTI35_Recon_max.nii.gz" %(self.path)):
            #odf_, max_, dwi_, b0 files should exist
            MsgUser.skipped("odf_recon output exists")
        else:
            
            cmdArray=["odf_recon","%s/Tractography/DTI35_eddy.nii.gz" %(self.path),"31","181","%s/Tractography/DTI35_Recon" %(self.path),"-b0", "5","-mat","%s/Tractography/temp_mat.dat" %(self.path),"-p","3","-sn", "1", "-ot", "nii.gz"]
            print(cmdArray)
            subprocess.call(cmdArray)

            MsgUser.ok("odf_recon Completed")
            
    def odf_tracker(self):
        MsgUser.bold("odf_tracker")
        #output: DTI35_Recon_max.nii.gz
        
        if (self.rebuild!=True and os.path.isfile("%s/Tractography/DTI35_Recon_dwi.nii.gz" %(self.path)) == False):
            MsgUser.failed("odf_tracker cannot be completed, odf_recon did not finish, missing DTI35_Recon files")
            return
            
        if self.rebuild!=True  and os.path.isfile("%s/Tractography/DTI35_preReg.trk" %(self.path)):
            #odf_, max_, dwi_, b0 files should exist
            MsgUser.skipped("odf_tracker output exists")
        else:
            cmdArray=["odf_tracker","%s/Tractography/DTI35_Recon" %(self.path),"%s/Tractography/DTI35_preReg.trk" %(self.path),"-at","45","-m", "%s/Tractography/DTI35_Recon_dwi.nii.gz" %(self.path),"-it","nii.gz"]
            print(cmdArray)
            subprocess.call(cmdArray)

            MsgUser.ok("odf_tracker Completed")
            
    def flirt(self):
        MsgUser.bold("flirt")
        #output: RegTransform4D
        

        if self.rebuild!=True  and os.path.isfile("%s/Tractography/RegTransform4d" %(self.path)):        
            MsgUser.skipped("flirt output exists")
        else:
            #flirt -in ./DTI35_eddy.nii.gz -ref ./brainmask.nii -omat ./RegTransform4D
            cmdArray=["flirt","-in","%s/Tractography/DTI35_eddy.nii.gz" %(self.path),"-ref","%s/Freesurfer/mri/brainmask.nii" %(self.path),"-omat","%s/Tractography/RegTransform4d" %(self.path)]
            print(cmdArray)
            subprocess.call(cmdArray)

            MsgUser.ok("flirt Completed")
            
    def tract_transform(self):
        MsgUser.bold("tract_transform")
        #output: DTI35_postReg.trk
        if self.rebuild!=True  and os.path.isfile("%s/Tractography/DTI35_postReg.trk" %(self.path)):#TODO Need correct filename
            #odf_, max_, dwi_, b0 files should exist
            MsgUser.skipped("tract_transform output exists")
        else:
            #track_transform DTI35_preReg.trk DTI35_postReg.trk -src DTI35_Recon_dwi.nii.gz -ref brainmask.nii -reg RegTransform4D

            cmdArray=["track_transform","%s/Tractography/DTI35_preReg.trk" %(self.path),"%s/Tractography/crush.trk" %(self.path),"-src","%s/Tractography/DTI35_Recon_dwi.nii.gz"%(self.path),"-ref", "%s/Freesurfer/mri/brainmask.nii" %(self.path),"-reg","%s/Tractography/RegTransform4D"%(self.path)]
            print(cmdArray)
            subprocess.call(cmdArray)

            MsgUser.ok("tract_transform Completed")
            
    def dti_recon(self):
        MsgUser.bold("dti_recon")
        if self.rebuild!=True  and os.path.isfile("%s/Tractography/DTI35_Reg2Brain_fa.nii" %(self.path)):#TODO we could test for all files to be sure
            #odf_, max_, dwi_, b0 files should exist
            MsgUser.skipped("dti_recon output exists")
        else:
            defaultGradientMatrix ="%s/%s" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),"gradientMatrix.txt")
            
            
            #dti_recon "%s/Tractography/DTI35_eddy.nii.gz" %(self.path) "%s/Tractography/dave/DTI35_Reg2Brain" %(self.path) -gm "%s" %(defaultGradientMatrix) -b 1000 -b0 5 -p 3 -sn 1 -ot nii 

            cmdArray=["dti_recon","%s/Tractography/DTI35_eddy.nii.gz" %(self.path),"%s/Tractography/DTI35_Reg2Brain" %(self.path),"-gm",defaultGradientMatrix,"-b", "1000","-b0","5","-p","3","-sn","1","-ot","nii"]
            print(cmdArray)
            subprocess.call(cmdArray)

            MsgUser.ok("dti_recon Completed")
            
       
    def dti_tracker(self):
        MsgUser.bold("dti_tracker")

        if self.rebuild!=True  and os.path.isfile("%s/Tractography/crush.trk" %(self.path)):
            MsgUser.skipped("dti_tracker output exists")
        else:
            #dti_tracker DTI35_Reg2Brain DTI35_postReg.trk -m DTI35_Reg2Brain_fa.nii 0.15

            cmdArray=["dti_tracker","%s/Tractography/DTI35_Reg2Brain" %(self.path),"%s/Tractography/crush.trk" %(self.path),"-m","%s/Tractography/DTI35_Reg2Brain_fa.nii"%(self.path),"-at","35","-m","%s/Tractography/DTI35_Reg2Brain_dwi.nii" %(self.path),"-it","nii"]
            print(cmdArray)
            subprocess.call(cmdArray)

            MsgUser.ok("dti_tracker Completed")
            
    def trackvis_worker(self,segment,counterpart,method):
        print("Rendering %s against %s using method %s" % (segment,counterpart,method))
        #track_vis ./DTI35_postReg_Threshold5.trk -roi_end ./wmparc3001.nii.gz -roi_end2 ./wmparc3002.nii.gz -nr
        
        if os.path.isfile("%s/Tractography/wmparc%s.nii.gz" %(self.path,segment)) and os.path.isfile("%s/Tractography/wmparc%s.nii.gz" %(self.path,counterpart)):
            if os.path.isfile("%s/Tractography/crush/%s-%s-%s.nii.txt" %(self.path,segment,counterpart,method)) == False:
                
                #trackvis = ["track_vis","%s/Tractography/crush.%s.trk" %(self.path,tmpFile),"-%s"%(method),"%s/Tractography/wmparc%s.nii.gz" %(self.path,segment),"-%s2" %(method),"%s/Tractography/wmparc%s.nii.gz" %(self.path,counterpart),"-nr", "-ov","%s/Tractography/crush/%s-%s-%s.nii" %(self.path,segment,counterpart,method)]
                trackvis = ["track_vis","%s/Tractography/crush.trk" %(self.path),"-%s"%(method),"%s/Tractography/wmparc%s.nii.gz" %(self.path,segment),"-%s2" %(method),"%s/Tractography/wmparc%s.nii.gz" %(self.path,counterpart),"-nr", "-ov","%s/Tractography/crush/%s-%s-%s.nii" %(self.path,segment,counterpart,method)]

                with open("%s/Tractography/crush/%s-%s-%s.nii.txt" %(self.path,segment,counterpart,method), "w") as track_vis_out:
                    proc = subprocess.Popen(trackvis, stdout=track_vis_out)
                    proc.communicate()
                #    os.remove("%s/Tractography/crush.%s.trk" %(self.path,tmpFile)) 
                with open ("%s/Tractography/crush/%s-%s-%s.nii.txt" %(self.path,segment,counterpart,method), "r") as myfile:
                    data=myfile.read()
                                                
            else:
                with open ("%s/Tractography/crush/%s-%s-%s.nii.txt" %(self.path,segment,counterpart,method), "r") as myfile:
                    data=myfile.read()#.replace('\n', '')

            with open("%s/Tractography/crush/tracts.txt" % (self.path), "a") as crush_file:
                ############
                
                m = re.search(r'Number of tracks: (\d+)', data)
                if m:
                    NumTracts = m.group(1).strip()
                else:
                    NumTracts = 0
                crush_file.write("%s-%s-%s-NumTracts=%s\n" % (segment,counterpart,method,NumTracts))                
                ############
                
                m = re.search(r'Number of tracks to render: (\d+)', data)
                if m:
                    TractsToRender = m.group(1).strip()
                else:
                    TractsToRender = 0
                crush_file.write("%s-%s-%s-TractsToRender=%s\n" % (segment,counterpart,method,TractsToRender))
                ############
                
                m = re.search(r'Number of line segments to render: (\d+)', data)
                if m:
                    LinesToRender = m.group(1).strip()
                else:
                    LinesToRender = 0
                crush_file.write("%s-%s-%s-LinesToRender=%s\n" % (segment,counterpart,method,LinesToRender))
                ############
                
                m = re.search(r'Mean track length: (\d+.\d+) +/- (\d+.\d+)', data)
                if m:
                    MeanTractLen = m.group(1).strip()
                    MeanTractLen_StdDev = m.group(2).strip()
                else:
                    MeanTractLen = 0
                    MeanTractLen_StdDev = 0
                crush_file.write("%s-%s-%s-MeanTractLen=%s\n" % (segment,counterpart,method,MeanTractLen))
                crush_file.write("%s-%s-%s-MeanTractLen_StdDev=%s\n" % (segment,counterpart,method,MeanTractLen_StdDev))
                ############
                
                m = re.search(r'Voxel Size: (\d*[.,]?\d*) (\d*[.,]?\d*) (\d*[.,]?\d*)', data)
                if m:
                    VoxelSizeX = m.group(1).strip()
                    VoxelSizeY = m.group(2).strip()
                    VoxelSizeZ = m.group(3).strip()
                else:
                    VoxelSizeX = 0
                    VoxelSizeY = 0
                    VoxelSizeZ = 0

                crush_file.write("%s-%s-%s-VoxelSizeX=%s\n" % (segment,counterpart,method,VoxelSizeX))
                crush_file.write("%s-%s-%s-VoxelSizeY=%s\n" % (segment,counterpart,method,VoxelSizeY))
                crush_file.write("%s-%s-%s-VoxelSizeZ=%s\n" % (segment,counterpart,method,VoxelSizeZ))
                
                #FA Mean
                #MsgUser.bold("FA Mean")
                meanFA=self.nonZeroMean("%s/Tractography/DTI35_Reg2Brain_fa.nii" %(self.path),"%s/Tractography/crush/%s-%s-%s.nii" %(self.path,segment,counterpart,method))             
                crush_file.write("%s-%s-%s-meanFA=%s\n" % (segment,counterpart,method,meanFA))
                #FA Std Dev
                #MsgUser.bold("FA Standard Deviation")
                
                stddevFA=self.nonZeroStdDev("%s/Tractography/DTI35_Reg2Brain_fa.nii" %(self.path),"%s/Tractography/crush/%s-%s-%s.nii" %(self.path,segment,counterpart,method))         
                crush_file.write("%s-%s-%s-stddevFA=%s\n" % (segment,counterpart,method,stddevFA))

                #ADC Mean
                #MsgUser.bold("ADC Mean")
                
                meanADC=self.nonZeroMean("%s/Tractography/DTI35_Reg2Brain_adc.nii" %(self.path),"%s/Tractography/crush/%s-%s-%s.nii" %(self.path,segment,counterpart,method))         
                crush_file.write("%s-%s-%s-meanADC=%s\n" % (segment,counterpart,method,meanADC))
                #ADC Std Dev
                #MsgUser.bold("ADC Standard Deviation")
                
                stddevADC=self.nonZeroStdDev("%s/Tractography/DTI35_Reg2Brain_adc.nii" %(self.path),"%s/Tractography/crush/%s-%s-%s.nii" %(self.path,segment,counterpart,method))       
                crush_file.write("%s-%s-%s-stddevADC=%s\n" % (segment,counterpart,method,stddevADC))
                
                ############# CLEANUP #################
                if os.path.isfile("%s/Tractography/crush/%s-%s-%s.nii" %(self.path,segment,counterpart,method)) == True:
                    os.remove("%s/Tractography/crush/%s-%s-%s.nii" %(self.path,segment,counterpart,method))
        else:
            MsgUser.failed("Parcellation (wmparc####.nii) files missing (%s or %s)"%(segment,counterpart))

    def track_vis(self):
        MsgUser.bold("track_vis")
        #output: crush.txt		
        
        no_of_procs = multiprocessing.cpu_count() 

        print("Multiprocessing across %s async procs" %(no_of_procs))
        
        
        pool = Pool(no_of_procs)
        if self.rebuild!=True  and os.path.isfile("%s/Tractography/crush/tracts.txt" %(self.path)):   
            
            if(self.fixmissing!=True):
                if(self.recrush):
                    print("Deleting previous crush output")
                    
                    folder = '%s/Tractography/crush' %(self.path)
                    for the_file in os.listdir(folder):
                        file_path = os.path.join(folder, the_file)
                        try:
                            if os.path.isfile(file_path):
                                os.unlink(file_path)        
                        except Exception as e:
                            print(e)
                else:
                    MsgUser.skipped("track_vis output exists")
                    return
            else:
                MsgUser.skipped("some track_vis output exists, I will crush anything missing")
                
        if not os.path.exists("%s/Tractography/crush/" % (self.path)):
            os.makedirs("%s/Tractography/crush/" % (self.path))

        #print(self.Segments)
        for s in self.Segments:
            segment=s['roi']
            segmentName=s['roiname']                                            
            for c in self.Segments:
                counterpart=c['roi']
                counterpartName=c['roiname']                               
                if (segment!=counterpart and segment<counterpart):                        
                    methods=[]  #Methods represents the possible ROI switches to trackvis, e.g methods = ["roi","roi_end"]
                    methodFile="%s/%s" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),"methods.txt")
                    with open(methodFile) as fin:
                        reader=csv.reader(fin, skipinitialspace=True, quotechar="'")
                        p = re.compile('^ *#')   # if not commented          
                        for row in reader:
                            if(not p.match(row[0])):                    
                                methods.append(row[0])                    
                    for method in methods:
                        #print("Rendering segment %s counterpart %s method %s" %(segment, counterpart, method))
                        pool.apply_async(self.trackvis_worker,(segment,counterpart,method))                                    
        pool.join()
        
        self.MeasurementComplete=True
        MsgUser.ok("track_vis Completed")

    
    def nonZeroMean(self,faFile,roiFile):
        
        if os.path.isfile(faFile) == False:        
            MsgUser.failed("%s is MISSING" %(faFile))
            return
        if os.path.isfile(roiFile) == False:        
            MsgUser.failed("%s is MISSING" %(roiFile))
            return

        imgFA = nib.load(faFile) #Untouched
        dataFA = imgFA.get_data()
        
        img = nib.load(roiFile)
        roiData = img.get_data()

        indecesOfInterest = np.nonzero(roiData)

        #I expect to see runtime warnings in this block, e.g. divide by zero
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)            
            mean =np.mean(dataFA[indecesOfInterest],dtype=np.float64)

        return mean
    def nonZeroStdDev(self,faFile,roiFile):
        
        if os.path.isfile(faFile) == False:        
            MsgUser.failed("%s is MISSING" %(faFile))
            return
        if os.path.isfile(roiFile) == False:        
            MsgUser.failed("%s is MISSING" %(roiFile))
            return

        imgFA = nib.load(faFile) #Untouched
        dataFA = imgFA.get_data()

        img = nib.load(roiFile)
        roiData = img.get_data()

        indecesOfInterest = np.nonzero(roiData)

        #I expect to see runtime warnings in this block, e.g. Degrees of freedom <= 0 for slice
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)            
            std =np.std(dataFA[indecesOfInterest],dtype=np.float64)

        return std
    
