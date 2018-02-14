import os, sys,inspect
import subprocess
#from pathlib import Path
from ux import MsgUser

                     
                
class Visit:
     #ReconComplete provides an indication if freesurfer recon-all has been run
    def __init__(self,path):
        self.Id=os.path.basename(path)
        self.path=path
        
        reconTest= "%s/mri/wmparc.mgz" % (path)
        if os.path.isfile(reconTest):
            self.ReconComplete=True
        else:
            self.ReconComplete=False
            
     
    def Render(self):
        #Lets Render as needed
        MsgUser.message("Rendering %s" % self.path)
        

        self.mgz2nifti()
        self.hardi_mat()
        self.odf_recon()
        self.odf_tracker()
        self.track_transform()
            
        
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
            
            subprocess.call(["odf_recon","%s/DTI35_eddy.nii.gz" %(self.path),"31","181","DTI35_Recon","-b0", "5","-mat","%s/temp_mat.dat" %(self.path),"-p","3","-sn", "1", "-ot", "nii.gz"])

            MsgUser.ok("odf_recon Completed")
            
    def odf_tracker(self):
        #output: DTI35_Recon_max.nii.gz
        
        if os.path.isfile("%s/Tractography/DTI35_Recon_dwi.nii.gz" %(self.path)):
            MsgUser.failed("odf_tracker cannot be completed, odf_recon did not finish, missing DTI35_Recon files")
            return
            
        if os.path.isfile("%s/Tractography/--TODO--DTI35_Recon_max.nii.gz" %(self.path)):
            #odf_, max_, dwi_, b0 files should exist
            MsgUser.skipped("odf_tracker output exists")
        else:
            
            subprocess.call(["odf_tracker","%s/DTI35_Recon" %(self.path),"%s/DTI35_preReg.trk" %(self.path),"-at","45","-m", "%s/DTI35_Recon_dwi.nii.gz" %(self.path),"-it","nii.gz"])

            MsgUser.ok("odf_tracker Completed")
            
    def track_transform(self):
        #output: DTI35_Recon_max.nii.gz
        if os.path.isfile("%s/Tractography/--TODO--DTI35_Recon_max.nii.gz" %(self.path)):
            #odf_, max_, dwi_, b0 files should exist
            MsgUser.skipped("track_transform output exists")
        else:
            #track_transform DTI35_preReg.trk DTI35_postReg.trk -src DTI35_Recon_dwi.nii.gz -ref brainmask.nii -reg RegTransform4D

            subprocess.call(["track_transform","%s/DTI35_preReg.trk" %(self.path),"%s/DTI35_postReg.trk" %(self.path),"-src","%s/DTI35_Recon_dwi.nii.gz"%(self.path),"-ref", "%s/brainmask.nii" %(self.path),"-reg","%s/RegTransform4D"%(self.path)])

            MsgUser.ok("track_transform Completed")
            
        