import os, sys,inspect
import subprocess
#from pathlib import Path
from ux import MsgUser
from brain import Measurement,Brain

                     
                
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
        self.flirt()
        self.track_vis()
            
        
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
            
    def track_transform(self):
        #output: DTI35_Recon_max.nii.gz
        if os.path.isfile("%s/Tractography/DTI35_Recon_max.nii.gz" %(self.path)):#TODO Need correct filename
            #odf_, max_, dwi_, b0 files should exist
            MsgUser.skipped("track_transform output exists")
        else:
            #track_transform DTI35_preReg.trk DTI35_postReg.trk -src DTI35_Recon_dwi.nii.gz -ref brainmask.nii -reg RegTransform4D

            subprocess.call(["track_transform","%s/DTI35_preReg.trk" %(self.path),"%s/DTI35_postReg.trk" %(self.path),"-src","%s/DTI35_Recon_dwi.nii.gz"%(self.path),"-ref", "%s/brainmask.nii" %(self.path),"-reg","%s/RegTransform4D"%(self.path)])

            MsgUser.ok("track_transform Completed")
            
    def flirt(self):
        #output: RegTransform4D
        if os.path.isfile("%s/Tractography/RegTransform4d" %(self.path)):        
            MsgUser.skipped("flirt output exists")
        else:
            #flirt -in ./DTI35_eddy.nii.gz -ref ./brainmask.nii -omat ./RegTransform4D

            subprocess.call(["flirt","-in","%s/Tractography/DTI35_eddy.nii.gz" %(self.path),"-ref","%s/Tractography/brainmask.nii" %(self.path),"-omat","%s/Tractography/RegTransform4d" %(self.path)])

            MsgUser.ok("flirt Completed")
            
    def track_vis(self):
        #output: atlas.txt
        if os.path.isfile("%s/atlas/atlas.txt" %(self.path)):        
            MsgUser.skipped("atlas output exists")
        else:
            
            B=Brain()

            for segment,segmentName in B.Segments.iteritems():
                for counterpart,counterpartName in B.Segments.iteritems():
                    
                    if (segment!=counterpart):
                        print("Rendering %s against %s" % (segment,counterpart))
                        #track_vis ./DTI35_postReg_Threshold5.trk -roi_end ./wmparc3001.nii.gz -roi_end2 ./wmparc3002.nii.gz -nr
                                  
                        if os.path.isfile("%s/Tractography/wmparc%s.nii.gz" %(self.path,segment)) and os.path.isfile("%s/Tractography/wmparc%s.nii.gz" %(self.path,counterpart)):
                            trackvis = ["track_vis","%s/Tractography/DTI35_postReg_Threshold5.trk" %(self.path),"-roi_end","%s/Tractography/wmparc%s.nii.gz" %(self.path,segment),"-roi_end2","%s/Tractography/wmparc%s.nii.gz" %(self.path,counterpart),"-nr"]
                            proc = subprocess.Popen(trackvis, stdout=subprocess.PIPE)
                            output = proc.stdout.read()
                            M=Measurement()
                            M.NaturallyTerminate(output)

                            print("\tNumber of tracks:%s"%(M.Number_of_Tracks))
                            print("\tNumber of tracks to render:%s"%(M.Number_of_Tracks_to_Render))
                            print("\tNumber of Segments to Render:%s"%(M.Number_of_Line_Segments_to_Render))
                            print("\tMean Track Length:%s +/- %s"%(M.Mean_Track_Length,M.Mean_Track_Length_ErrBar))
                            print("\tVolume Dimension:%s %s %s"%(M.Volume_Dimension_X,M.Volume_Dimension_Y,M.Volume_Dimension_Z))
                            print("\tVoxel Size: %s %s %s"%(M.Voxel_Size_X,M.Voxel_Size_Y,M.Voxel_Size_Z))
                            #print output
                        else:
                            MsgUser.failed("Segment files missing (%s or %s)"%(segment,counterpart))
            MsgUser.ok("track_vis Completed")