import os, sys,inspect
import subprocess
import re
#from pathlib import Path
from ux import MsgUser
#import nibabel as nib
import numpy as np


              
class Visit:
   
        
    def __init__(self,path,rebuild,voi):
       
        self.Id=os.path.basename(path)
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
                         "3003":"wm-lh-caudalmiddlefrontal",
                         "3007":"wm-lh-fusiform",
                        # "1034":"ctx-lh-transversetemporal",
                         "1035":"ctx-lh-insula"
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
            print cmdArray
            subprocess.call(cmdArray)
            
            MsgUser.ok("eddy_correct Completed")

            
        
    def hardi_mat(self):
        MsgUser.bold("hardi_mat")
        if self.rebuild!=True and os.path.isfile("%s/Tractography/temp_mat.dat" %(self.path)):
            MsgUser.skipped("hardi_mat output exists")
        else:
            defaultGradientMatrix ="%s/%s" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),"gradientMatrix.txt")
            
            cmdArray=["hardi_mat",defaultGradientMatrix,"%s/Tractography/temp_mat.dat" % (self.path), "-ref","%s/Tractography/DTI35_eddy.nii.gz" % (self.path),"-oc"]
            print cmdArray
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
            print cmdArray
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
            print cmdArray
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
            print cmdArray
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
            print cmdArray
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
            print cmdArray
            subprocess.call(cmdArray)

            MsgUser.ok("dti_recon Completed")
            
       
    def dti_tracker(self):
        MsgUser.bold("dti_tracker")

        if self.rebuild!=True  and os.path.isfile("%s/Tractography/crush.trk" %(self.path)):
            MsgUser.skipped("dti_tracker output exists")
        else:
            #dti_tracker DTI35_Reg2Brain DTI35_postReg.trk -m DTI35_Reg2Brain_fa.nii 0.15

            cmdArray=["dti_tracker","%s/Tractography/DTI35_Reg2Brain" %(self.path),"%s/Tractography/crush.trk" %(self.path),"-m","%s/Tractography/DTI35_Reg2Brain_fa.nii"%(self.path),"-at","35","-m","%s/Tractography/DTI35_Reg2Brain_dwi.nii" %(self.path),"-it","nii"]
            print cmdArray
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
 
            for segment,segmentName in self.Segments.iteritems():
                for counterpart,counterpartName in self.Segments.iteritems():
                    
                    if (segment!=counterpart and segment<counterpart):
                        methods = ["roi","roi_end"]
                        for method in methods:
                            print("Rendering %s against %s using method %s" % (segment,counterpart,method))
                            #track_vis ./DTI35_postReg_Threshold5.trk -roi_end ./wmparc3001.nii.gz -roi_end2 ./wmparc3002.nii.gz -nr

                            if os.path.isfile("%s/Tractography/wmparc%s.nii.gz" %(self.path,segment)) and os.path.isfile("%s/Tractography/wmparc%s.nii.gz" %(self.path,counterpart)):
                                if os.path.isfile("%s/Tractography/crush/%s-%s-%s.nii.txt" %(self.path,segment,counterpart,method)) == False:
                                    trackvis = ["track_vis","%s/Tractography/crush.trk" %(self.path),"-%s"%(method),"%s/Tractography/wmparc%s.nii.gz" %(self.path,segment),"-%s2" %(method),"%s/Tractography/wmparc%s.nii.gz" %(self.path,counterpart),"-nr", "-ov","%s/Tractography/crush/%s-%s-%s.nii" %(self.path,segment,counterpart,method)]
                                    print trackvis
                                    proc = subprocess.Popen(trackvis, stdout=subprocess.PIPE)
                                    data = proc.stdout.read()
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
    
