import os, sys,inspect
import subprocess
import numpy as np
import re

#from pathlib import Path
from tractcrush.ux import MsgUser
import nibabel as nib


              
class Visit:
   
        
    def __init__(self,path,rebuild,voi):
       
        self.VisitId=os.path.basename(path)
        self.path=path
        self.rebuild=rebuild
        self.voi=voi
        self.MeasurementComplete=False
        reconTest= "%s/Freesurfer/mri/wmparc.mgz" % (path)
        if os.path.isfile(reconTest):
            self.ReconComplete=True
        else:
            self.ReconComplete=False
            
        self.Segments = {
                        #"3002":"wm-lh-caudalanteriorcingulate ",
                        # "3003":"wm-lh-caudalmiddlefrontal",
                        # "3007":"wm-lh-fusiform",
                        # "1034":"ctx-lh-transversetemporal",
                        # "1035":"ctx-lh-insula"
                        "0002":"TBD",
                        "0004":"TBD",
                        "0005":"TBD",
                        "0007":"TBD",
                        "0008":"TBD",
                        "0010":"TBD",
                        "0011":"TBD",
                        "0012":"TBD",
                        "0013":"TBD",
                        "0014":"TBD",
                        "0015":"TBD",
                        "0016":"TBD",
                        "0017":"TBD",
                        "0018":"TBD",
                        "0024":"TBD",
                        "0026":"TBD",
                        "0028":"TBD",
                        "0030":"TBD",
                        "0031":"TBD",
                        "0041":"TBD",
                        "0043":"TBD",
                        "0044":"TBD",
                        "0046":"TBD",
                        "0047":"TBD",
                        "0049":"TBD",
                        "0050":"TBD",
                        "0051":"TBD",
                        "0052":"TBD",
                        "0053":"TBD",
                        "0054":"TBD",
                        "0058":"TBD",
                        "0060":"TBD",
                        "0062":"TBD",
                        "0063":"TBD",
                        "0077":"TBD",
                        "0085":"TBD",
                        "0251":"TBD",
                        "0252":"TBD",
                        "0253":"TBD",
                        "0254":"TBD",
                        "0255":"TBD",
                        "1000":"TBD",
                        "1001":"TBD",
                        "1002":"TBD",
                        "1003":"TBD",
                        "1005":"TBD",
                        "1006":"TBD",
                        "1007":"TBD",
                        "1008":"TBD",
                        "1009":"TBD",
                        "1010":"TBD",
                        "1011":"TBD",
                        "1012":"TBD",
                        "1013":"TBD",
                        "1014":"TBD",
                        "1015":"TBD",
                        "1016":"TBD",
                        "1017":"TBD",
                        "1018":"TBD",
                        "1019":"TBD",
                        "1020":"TBD",
                        "1021":"TBD",
                        "1022":"TBD",
                        "1023":"TBD",
                        "1024":"TBD",
                        "1025":"TBD",
                        "1026":"TBD",
                        "1027":"TBD",
                        "1028":"TBD",
                        "1029":"TBD",
                        "1030":"TBD",
                        "1031":"TBD",
                        "1032":"TBD",
                        "1033":"TBD",
                        "1034":"TBD",
                        "1035":"TBD",
                        "2000":"TBD",
                        "2001":"TBD",
                        "2002":"TBD",
                        "2003":"TBD",
                        "2005":"TBD",
                        "2006":"TBD",
                        "2007":"TBD",
                        "2008":"TBD",
                        "2009":"TBD",
                        "2010":"TBD",
                        "2011":"TBD",
                        "2012":"TBD",
                        "2013":"TBD",
                        "2014":"TBD",
                        "2015":"TBD",
                        "2016":"TBD",
                        "2017":"TBD",
                        "2018":"TBD",
                        "2019":"TBD",
                        "2020":"TBD",
                        "2021":"TBD",
                        "2022":"TBD",
                        "2023":"TBD",
                        "2024":"TBD",
                        "2025":"TBD",
                        "2026":"TBD",
                        "2027":"TBD",
                        "2028":"TBD",
                        "2029":"TBD",
                        "2030":"TBD",
                        "2031":"TBD",
                        "2032":"TBD",
                        "2033":"TBD",
                        "2034":"TBD",
                        "2035":"TBD",
                        "3001":"TBD",
                        "3002":"TBD",
                        "3003":"TBD",
                        "3005":"TBD",
                        "3006":"TBD",
                        "3007":"TBD",
                        "3008":"TBD",
                        "3009":"TBD",
                        "3010":"TBD",
                        "3011":"TBD",
                        "3012":"TBD",
                        "3013":"TBD",
                        "3014":"TBD",
                        "3015":"TBD",
                        "3016":"TBD",
                        "3017":"TBD",
                        "3018":"TBD",
                        "3019":"TBD",
                        "3020":"TBD",
                        "3021":"TBD",
                        "3022":"TBD",
                        "3023":"TBD",
                        "3024":"TBD",
                        "3025":"TBD",
                        "3026":"TBD",
                        "3027":"TBD",
                        "3028":"TBD",
                        "3029":"TBD",
                        "3030":"TBD",
                        "3031":"TBD",
                        "3032":"TBD",
                        "3033":"TBD",
                        "3034":"TBD",
                        "3035":"TBD",
                        "4001":"TBD",
                        "4002":"TBD",
                        "4003":"TBD",
                        "4005":"TBD",
                        "4006":"TBD",
                        "4007":"TBD",
                        "4008":"TBD",
                        "4009":"TBD",
                        "4010":"TBD",
                        "4011":"TBD",
                        "4012":"TBD",
                        "4013":"TBD",
                        "4014":"TBD",
                        "4015":"TBD",
                        "4016":"TBD",
                        "4017":"TBD",
                        "4018":"TBD",
                        "4019":"TBD",
                        "4020":"TBD",
                        "4021":"TBD",
                        "4022":"TBD",
                        "4023":"TBD",
                        "4024":"TBD",
                        "4025":"TBD",
                        "4026":"TBD",
                        "4027":"TBD",
                        "4028":"TBD",
                        "4029":"TBD",
                        "4030":"TBD",
                        "4031":"TBD",
                        "4032":"TBD",
                        "4033":"TBD",
                        "4034":"TBD",
                        "4035":"TBD",
                        "5001":"TBD",
                        "5002":"TBD"
                        }
                    
     
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


                #Print results
                row=[]
                row.append(os.path.split(os.path.dirname(self.path))[1])
                row.append(self.VisitId)
                for cell in content:
                    if cell in measures:
                        row.append(measures[cell].strip())
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
            
        
    def track_vis(self):
        MsgUser.bold("track_vis")
        #output: crush.txt		
        if self.rebuild!=True  and os.path.isfile("%s/Tractography/crush/tracts.txt" %(self.path)):        
            MsgUser.skipped("track_vis output exists")
        else:
            if not os.path.exists("%s/Tractography/crush/" % (self.path)):
                os.makedirs("%s/Tractography/crush/" % (self.path))
 
            for segment,segmentName in self.Segments.items():
                for counterpart,counterpartName in self.Segments.items():
                    
                    if (segment!=counterpart and segment<counterpart):
                        methods = ["roi","roi_end"]
                        for method in methods:
                            print("Rendering %s against %s using method %s" % (segment,counterpart,method))
                            #track_vis ./DTI35_postReg_Threshold5.trk -roi_end ./wmparc3001.nii.gz -roi_end2 ./wmparc3002.nii.gz -nr

                            if os.path.isfile("%s/Tractography/wmparc%s.nii.gz" %(self.path,segment)) and os.path.isfile("%s/Tractography/wmparc%s.nii.gz" %(self.path,counterpart)):
                                if os.path.isfile("%s/Tractography/crush/%s-%s-%s.nii.txt" %(self.path,segment,counterpart,method)) == False:
                                    trackvis = ["track_vis","%s/Tractography/crush.trk" %(self.path),"-%s"%(method),"%s/Tractography/wmparc%s.nii.gz" %(self.path,segment),"-%s2" %(method),"%s/Tractography/wmparc%s.nii.gz" %(self.path,counterpart),"-nr", "-ov","%s/Tractography/crush/%s-%s-%s.nii" %(self.path,segment,counterpart,method)]
                                    print(trackvis)
                                    proc = subprocess.Popen(trackvis, stdout=subprocess.PIPE)
                                    data = str(proc.stdout.read())
                                    with open("%s/Tractography/crush/%s-%s-%s.nii.txt" %(self.path,segment,counterpart,method), "w") as track_vis_out:
                                        track_vis_out.write(data)
                                #print data
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
        std =np.std(dataFA[indecesOfInterest],dtype=np.float64)

        return std
    
