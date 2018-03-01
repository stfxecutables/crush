import os, sys,inspect
import subprocess
import re
#from pathlib import Path
from ux import MsgUser
import nibabel as nib
import numpy as np


              
class Visit:
   
        
    def __init__(self,path):
       
        self.Id=os.path.basename(path)
        self.path=path
        
        reconTest= "%s/mri/wmparc.mgz" % (path)
        if os.path.isfile(reconTest):
            self.ReconComplete=True
        else:
            self.ReconComplete=False
            
        self.Segments = {"3002":"wm-lh-caudalanteriorcingulate ",
                         "3003":"wm-lh-caudalmiddlefrontal",
                         "3007":"wm-lh-fusiform"
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
        self.dti_tracker()
        
    def Measure(self):
    
        self.track_vis()
        self.FA()
            
        
    def mgz2nifti(self):  
        
        if os.path.isfile("%s/mri/aseg.nii" % (self.path)):
            self.NiftiComplete=True
            MsgUser.skipped("All Nifti files exist")
        else:
            MsgUser.warning("\tNifti Incomplete, rendering nii files...")
                 
            mgzFiles=['aseg','aparc+aseg', 'aparc.a2009s+aseg', 'lh.ribbon', 'rh.ribbon', 'nu', 'orig', 'ribbon', 'wm.asegedit', 'wm', 'wm.seg', 'brain', 'brainmask']
       
            for mgz in mgzFiles:
                if os.path.isfile("%s/mri/%s.nii" % (self.path,mgz)) and not replace:
                    MsgUser.skipped("\t%s.nii exists" % (mgz))
                else:
                
                    MsgUser.message("Create or replace %s.nii" % (mgz))
                    subprocess.call(['mri_convert','-rt','nearest','-nc','-ns','1',"%s/mri/%s.mgz" %(self.path,mgz),"%s/mri/%s.nii" % (self.path,mgz)])

    def eddy_correct(self):
        #eddy_correct ~/HealthyTractography/%s/%s/DTI35.nii ~/HealthyTractography/%s/%s/DTI35_eddy.nii 0
        
        if os.path.isfile("%s/Tractography/DTI35_eddy.nii.gz" %(self.path)):
            MsgUser.skipped("eddy_correct output exists")
        else:
            
            subprocess.call(["eddy_correct","%s/Tractography/DTI35.nii" % (self.path),"%s/Tractography/DTI35_eddy.nii.gz" % (self.path),"0"])
            
            MsgUser.ok("eddy_correct Completed")

            
        
    def hardi_mat(self):
        if os.path.isfile("%s/Tractography/temp_mat.dat" %(self.path)):
            MsgUser.skipped("hardi_mat output exists")
        else:
            defaultGradientMatrix ="%s/%s" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),"gradientMatrix.txt")
            
            subprocess.call(["hardi_mat",defaultGradientMatrix,"%s/Tractography/temp_mat.dat" % (self.path), "-ref","%s/Tractography/DTI35_eddy.nii.gz" % (self.path),"-oc"])
            
            MsgUser.ok("HARDIReconstruction Completed")

            
    def odf_recon(self):
        #output: DTI35_Recon_max.nii.gz
        if os.path.isfile("%s/Tractography/DTI35_Recon_max.nii.gz" %(self.path)):
            #odf_, max_, dwi_, b0 files should exist
            MsgUser.skipped("odf_recon output exists")
        else:
            
            subprocess.call(["odf_recon","%s/Tractography/DTI35_eddy.nii.gz" %(self.path),"31","181","DTI35_Recon","-b0", "5","-mat","%s/temp_mat.dat" %(self.path),"-p","3","-sn", "1", "-ot", "nii.gz"])

            MsgUser.ok("odf_recon Completed")
            
    def odf_tracker(self):
        #output: DTI35_Recon_max.nii.gz
        
        if (os.path.isfile("%s/Tractography/DTI35_Recon_dwi.nii.gz" %(self.path)) == False):
            MsgUser.failed("odf_tracker cannot be completed, odf_recon did not finish, missing DTI35_Recon files")
            return
            
        if os.path.isfile("%s/Tractography/DTI35_Recon_max.nii.gz" %(self.path)):
            #odf_, max_, dwi_, b0 files should exist
            MsgUser.skipped("odf_tracker output exists")
        else:
            
            subprocess.call(["odf_tracker","%s/Tractography/DTI35_Recon" %(self.path),"%s/DTI35_preReg.trk" %(self.path),"-at","45","-m", "%s/Tractography/DTI35_Recon_dwi.nii.gz" %(self.path),"-it","nii.gz"])

            MsgUser.ok("odf_tracker Completed")
            
    def flirt(self):
        #output: RegTransform4D
        if os.path.isfile("%s/Tractography/RegTransform4d" %(self.path)):        
            MsgUser.skipped("flirt output exists")
        else:
            #flirt -in ./DTI35_eddy.nii.gz -ref ./brainmask.nii -omat ./RegTransform4D

            subprocess.call(["flirt","-in","%s/Tractography/DTI35_eddy.nii.gz" %(self.path),"-ref","%s/Tractography/brainmask.nii" %(self.path),"-omat","%s/Tractography/RegTransform4d" %(self.path)])

            MsgUser.ok("flirt Completed")
            
    def tract_transform(self):
        #output: DTI35_Recon_max.nii.gz
        if os.path.isfile("%s/Tractography/DTI35_Recon_max.nii.gz" %(self.path)):#TODO Need correct filename
            #odf_, max_, dwi_, b0 files should exist
            MsgUser.skipped("tract_transform output exists")
        else:
            #track_transform DTI35_preReg.trk DTI35_postReg.trk -src DTI35_Recon_dwi.nii.gz -ref brainmask.nii -reg RegTransform4D

            subprocess.call(["track_transform","%s/DTI35_preReg.trk" %(self.path),"%s/DTI35_postReg.trk" %(self.path),"-src","%s/DTI35_Recon_dwi.nii.gz"%(self.path),"-ref", "%s/brainmask.nii" %(self.path),"-reg","%s/RegTransform4D"%(self.path)])

            MsgUser.ok("tract_transform Completed")
            
    def dti_tracker(self):
        MsgUser.skipped("dti_tracker TODO")
        #dti_tracker DTI35_Reg2Brain DTI35_postRegDAVE.trk -m DTI35_Reg2Brain_fa.nii 0.15
        
    def track_vis(self):
        #output: atlas.txt
        if os.path.isfile("%s/atlas/tracts.txt" %(self.path)):        
            MsgUser.skipped("track_vis output exists")
        else:
            if not os.path.exists("%s/atlas/" % (self.path)):
                os.makedirs("%s/atlas/" % (self.path))
 
            for segment,segmentName in self.Segments.iteritems():
                for counterpart,counterpartName in self.Segments.iteritems():
                    
                    if (segment!=counterpart):
                        print("Rendering %s against %s" % (segment,counterpart))
                        #track_vis ./DTI35_postReg_Threshold5.trk -roi_end ./wmparc3001.nii.gz -roi_end2 ./wmparc3002.nii.gz -nr
                                  
                        if os.path.isfile("%s/Tractography/wmparc%s.nii.gz" %(self.path,segment)) and os.path.isfile("%s/Tractography/wmparc%s.nii.gz" %(self.path,counterpart)):
                            trackvis = ["track_vis","%s/Tractography/DTI35_postReg.trk" %(self.path),"-roi_end","%s/Tractography/wmparc%s.nii.gz" %(self.path,segment),"-roi_end2","%s/Tractography/wmparc%s.nii.gz" %(self.path,counterpart),"-nr"]
                            proc = subprocess.Popen(trackvis, stdout=subprocess.PIPE)
                            data = proc.stdout.read()
                            #print data
                            with open("%s/atlas/tracts.txt" % (self.path), "w") as atlas_file:
                                ############
                                m = re.search(r'Number of tracks: (\d+)', data)
                                if m:
                                    NumTracts = m.group(1).strip()
                                else:
                                    NumTracts = 0
                                atlas_file.write("%s:%s:roi_end:roi_end2:NumTracts:%s\n" % (segment,counterpart,NumTracts))
                                ############
                                m = re.search(r'Number of tracks to render: (\d+)', data)
                                if m:
                                    TractsToRender = m.group(1).strip()
                                else:
                                    TractsToRender = 0
                                atlas_file.write("%s:%s:roi_end:roi_end2:TractsToRender:%s\n" % (segment,counterpart,TractsToRender))
                                ############
                                m = re.search(r'Number of line segments to render: (\d+)', data)
                                if m:
                                    LinesToRender = m.group(1).strip()
                                else:
                                    LinesToRender = 0
                                atlas_file.write("%s:%s:roi_end:roi_end2:LinesToRender:%s\n" % (segment,counterpart,LinesToRender))
                                ############
                                m = re.search(r'Mean track length: (\d+.\d+) +/- (\d+.\d+)', data)
                                if m:
                                    MeanTractLen = m.group(1).strip()
                                    MeanTractLen_StdDev = m.group(2).strip()
                                else:
                                    MeanTractLen = 0
                                    MeanTractLen_StdDev = 0
                                atlas_file.write("%s:%s:roi_end:roi_end2:MeanTractLen:%s\n" % (segment,counterpart,MeanTractLen))
                                atlas_file.write("%s:%s:roi_end:roi_end2:MeanTractLen_StdDev:%s\n" % (segment,counterpart,MeanTractLen_StdDev))
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
                                    
                                atlas_file.write("%s:%s:roi_end:roi_end2:VoxelSizeX:%s\n" % (segment,counterpart,VoxelSizeX))
                                atlas_file.write("%s:%s:roi_end:roi_end2:VoxelSizeY:%s\n" % (segment,counterpart,VoxelSizeY))
                                atlas_file.write("%s:%s:roi_end:roi_end2:VoxelSizeZ:%s\n" % (segment,counterpart,VoxelSizeZ))
                            
                            
                        else:
                            MsgUser.failed("Segment files missing (%s or %s)"%(segment,counterpart))
            MsgUser.ok("track_vis Completed")
    def FA(self):
        if os.path.isfile("%s/Tractography/DTI35_Reg2Brain_fa.nii" %(self.path)) == False:        
            MsgUser.failure("%s/Tractography/DTI35_Reg2Brain_fa.nii is MISSING" %(self.path))
        else:
       
            #print("%s/Tractography/wmparc3002.nii.gz" %(self.path))
            #wmparc = nib.load("%s/Tractography/wmparc3002.nii.gz" %(self.path))
            #wmparcData = wmparc.get_data()
            
            ##output: atlas.txt
            #if os.path.isfile("%s/atlas/fa.txt" %(self.path)):        
            #    MsgUser.skipped("fa output exists")
            #else:
            #    with open("%s/atlas/fa.txt" % (self.path), "w") as atlas_file:
            #        atlas_file.write("X")            
                
            ##print('wmparc data.shape (%d, %d, %d, %d)' % wmparcData.shape)
            ##print wmparc.get_data_shape()
            ##//print wmparcData
            
            imgFA = nib.load("%s/Tractography/DTI35_Reg2Brain_fa.nii" %(self.path)) #Untouched
            dataFA = imgFA.get_data()

            img = nib.load("%s/Tractography/1035-1034.nii"%(self.path))
            data = img.get_data()
            
            total=0
            count=0
            
            roi=np.multiply(dataFA,data)
            roiIndices =np.nonzero(roi)
            
            
            
            #print(meanThis.shape)
            mean =np.mean(roi[roiIndices])
            
            #meanThis[meanThis == 0] = np.nan
            #A(~A) = inf;  % Or A(A==0) = inf;
            #meanThis(~meanThis) = np.nan; % Or meanThis(meanThis==0) = np.nan
            #means = np.nanmean(meanThis[:, 1:], axis=1)
            #print means
            #mean=np.mean(means)
            print(mean)
            return
            for i in range(169,255):
                #print i
                for j in range(0,255):
                    for k in range(0,255):
                        if data[i,j,k]==1:
                            print("%d %d %d %d" %(i,j,k,1))
                            count+=1
                            total+=dataFA[i,j,k]
            print("total: %d  count:%d  mean:%d"%(total,count,total/count))
        return