import sys,os,subprocess
import re
import nibabel as nib
import numpy as np
import warnings

class workerTrackvis(object):

    def process(self,parr):#segment,counterpart,method):
            segment=parr[0]
            counterpart=parr[1]
            method=parr[2]
            tractographypath=parr[3]
            pipelineId=parr[4]

            calcs={}
            print('.',end='',flush=True)
            #print(".",end=".")

            #track_vis ./DTI35_postReg_Threshold5.trk -roi_end ./wmparc3001.nii.gz -roi_end2 ./wmparc3002.nii.gz -nr
            
            #create wmparc#### if missing
            wmparcStart=f"{tractographypath}/parcellations/wmparc{segment}.nii"
            wmparcEnd=f"{tractographypath}/parcellations/wmparc{counterpart}.nii"
            #if not os.path.isfile("%s/wmparc%s.nii.gz" %(tractographypath,segment)) and not os.path.isfile("%s/wmparc%s.nii.gz" %(tractographypath,counterpart)):
            #    MsgUser.warning("%s/wmparc%s.nii.gz" %(tractographypath,segment))

            #if os.path.isfile("%s/wmparc%s.nii.gz" %(tractographypath,segment)) and os.path.isfile("%s/wmparc%s.nii.gz" %(tractographypath,counterpart)):
            if os.path.isfile(wmparcStart) and os.path.isfile(wmparcEnd):

                render = True

                # if self.persistencemode !='db' and len(calcs)>0:
                #     MsgUser.ok("Previous calculations detected for %s,%s,%s" %(segment,counterpart,method))
                #     calcsJson = "%s/crush/%s/calcs-%s-%s-%s.json" % (tractographypath,segment,segment,counterpart,method)

                #     if not os.path.isdir("%s/crush/%s" % (tractographypath,segment)):
                #         os.mkdir("%s/crush/%s" % (tractographypath,segment))

                #     with open(calcsJson, "w") as calcs_file:
                #         json.dump(calcs,calcs_file)                        
                #         self.visit.trackvis_cleanup_nii(segment,counterpart,method)
                #     #MsgUser.skipped("SKIPPING already calculated measures for %s-%s-%s" %(segment,counterpart,method))
                #     return calcs
                # else:
                #     MsgUser.ok("Rendering missing measures for %s-%s-%s" %(segment,counterpart,method))

                wmparcStart=f"{tractographypath}/parcellations/wmparc{segment}.nii"
                wmparcEnd=f"{tractographypath}/parcellations/wmparc{counterpart}.nii"
                if os.path.isfile(wmparcStart) and os.path.isfile(wmparcEnd):
                    #if self.visit.disable_log:
                    #trackvis = ["track_vis","%s/crush.trk" %(tractographypath),"-%s"%(method),"%s/parcellations/wmparc%s.nii" %(tractographypath,segment),"-%s2" %(method),"%s/parcellations/wmparc%s.nii" %(tractographypath,counterpart),"-nr", "-ov","%s/crush/%s-%s-%s.nii" %(tractographypath,segment,counterpart,method),"-disable_log"]
                    trackvis = ["track_vis","%s/crush.trk" %(tractographypath),"-%s"%(method),"%s/parcellations/wmparc%s.nii" %(tractographypath,segment),"-%s2" %(method),"%s/parcellations/wmparc%s.nii" %(tractographypath,counterpart),"-nr", "-ov","%s/crush/%s-%s-%s.nii" %(tractographypath,segment,counterpart,method)]
                    print(trackvis)
                    #else:
                    #trackvis = ["track_vis","%s/crush.trk" %(tractographypath),"-%s"%(method),"%s/parcellations/wmparc%s.nii" %(tractographypath,segment),"-%s2" %(method),"%s/parcellations/wmparc%s.nii" %(tractographypath,counterpart),"-nr", "-ov","%s/crush/%s-%s-%s.nii" %(tractographypath,segment,counterpart,method)]
                    
                    if not os.path.isfile("%s/crush/%s-%s-%s.nii" %(tractographypath,segment,counterpart,method)):
                        if not os.path.isdir(f"{tractographypath}/crush/{segment}"):
                            os.mkdir(f"{tractographypath}/crush/{segment}")
                        try:
                            proc = subprocess.run(trackvis,capture_output=True, text=True)
#                            print(proc)
                            with open("%s/crush/%s/%s-%s-%s.nii.txt" %(tractographypath,segment,segment,counterpart,method), "w") as track_vis_out:
                                #proc = subprocess.Popen(trackvis, stdout=track_vis_out)
                                #proc.communicate() 
                                print(proc.stdout)
                                data=proc.stdout
                   #         if proc.returncode <> 0:
                   #             print("TRACKVIS Command returned non-zero exit code")


                        except Exception as e:
                            print(f"Trackvis failed::{e}")                            

                    with open ("%s/crush/%s/%s-%s-%s.nii.txt" %(tractographypath,segment,segment,counterpart,method), "r") as myfile:                        
                        data=myfile.read()                                   
                else:
                    data=""

                #data = self.trackvis_create_nii(segment,counterpart,method)
                
               
                m = re.search(r'Number of tracks: (\d+)', data)
                if m:
                    NumTracts = m.group(1).strip()
                else:
                    NumTracts = 0
                calcs["%s/%s-%s-%s-NumTracts" %(pipelineId,segment,counterpart,method)]=NumTracts
                
                ############
                
                m = re.search(r'Number of tracks to render: (\d+)', data)
                if m:
                    TractsToRender = m.group(1).strip()
                else:
                    TractsToRender = 0
                calcs["%s/%s-%s-%s-TractsToRender" %(pipelineId,segment,counterpart,method)]=TractsToRender
                
                ############
                
                m = re.search(r'Number of line segments to render: (\d+)', data)
                if m:
                    LinesToRender = m.group(1).strip()
                else:
                    LinesToRender = 0
                calcs["%s/%s-%s-%s-LinesToRender" %(pipelineId,segment,counterpart,method)]=LinesToRender
                ############
                
                m = re.search(r'Mean track length: (\d+.\d+) \+\/- (\d+.\d+)', data)
                if m:
                    MeanTractLen = m.group(1).strip()
                    MeanTractLen_StdDev = m.group(2).strip()
                else:
                    MeanTractLen = 0
                    MeanTractLen_StdDev = 0
                
                calcs["%s/%s-%s-%s-MeanTractLen" %(pipelineId,segment,counterpart,method)]=MeanTractLen
                calcs["%s/%s-%s-%s-MeanTractLen_StdDev" %(pipelineId,segment,counterpart,method)]=MeanTractLen_StdDev
                ############
                
                m = re.search(r'Voxel size: (\d*[.,]?\d*) (\d*[.,]?\d*) (\d*[.,]?\d*)', data)
                if m:
                    VoxelSizeX = m.group(1).strip()
                    VoxelSizeY = m.group(2).strip()
                    VoxelSizeZ = m.group(3).strip()
                else:
                    VoxelSizeX = 0
                    VoxelSizeY = 0
                    VoxelSizeZ = 0

                calcs["%s/%s-%s-%s-VoxelSizeX" %(pipelineId,segment,counterpart,method)]=VoxelSizeX
                calcs["%s/%s-%s-%s-VoxelSizeY" %(pipelineId,segment,counterpart,method)]=VoxelSizeY
                calcs["%s/%s-%s-%s-VoxelSizeZ" %(pipelineId,segment,counterpart,method)]=VoxelSizeZ

                
                #FA Mean
                meanFA=self.nonZeroMean("%s/DTI_Reg2Brain_fa.nii" %(tractographypath),"%s/crush/%s-%s-%s.nii" %(tractographypath,segment,counterpart,method))                             
                calcs["%s/%s-%s-%s-meanFA" %(pipelineId,segment,counterpart,method)]=meanFA
                
                #FA Std Dev
                stddevFA=self.nonZeroStdDev("%s/DTI_Reg2Brain_fa.nii" %(tractographypath),"%s/crush/%s-%s-%s.nii" %(tractographypath,segment,counterpart,method))         
                calcs["%s/%s-%s-%s-stddevFA" %(pipelineId,segment,counterpart,method)]=stddevFA            
                
                #ADC Mean
                meanADC=self.nonZeroMean("%s/DTI_Reg2Brain_adc.nii" %(tractographypath),"%s/crush/%s-%s-%s.nii" %(tractographypath,segment,counterpart,method))         
                calcs["%s/%s-%s-%s-meanADC" %(pipelineId,segment,counterpart,method)]=meanADC
                
                #ADC Std Dev
                stddevADC=self.nonZeroStdDev("%s/DTI_Reg2Brain_adc.nii" %(tractographypath),"%s/crush/%s-%s-%s.nii" %(tractographypath,segment,counterpart,method))       
                calcs["%s/%s-%s-%s-stddevADC" %(pipelineId,segment,counterpart,method)]=stddevADC
                
                

            else:
                #print("Parcellation (wmparc####.nii) files missing (%s or %s)"%(segment,counterpart))
                if not os.path.isfile(wmparcStart):
                    print("%s is missing for %s-%s operation" %(wmparcStart,segment,counterpart))
                if not os.path.isfile(wmparcEnd):
                    print("%s is missing for %s-%s operation" %(wmparcStart,segment,counterpart))
            
   
            
            # Cache CALCS to temp file because it's not written to tracts.txt until the join (after all ROIs finish)    
            # if self.persistencemode =='db':
            #     return calcs                       
            # else:
            #     if not os.path.isdir("%s/crush/%s" % (tractographypath,segment)):
            #         os.mkdir("%s/crush/%s" % (tractographypath,segment))

            #     calcsJson = "%s/crush/%s/calcs-%s-%s-%s.json" % (tractographypath,segment,segment,counterpart,method)
            #     with open(calcsJson, "w") as calcs_file:
            #         json.dump(calcs,calcs_file)
            #         ############# CLEANUP #################
            #        ### self.trackvis_cleanup_nii(segment,counterpart,method)

            nii = "%s/crush/%s-%s-%s.nii" %(tractographypath,segment,counterpart,method)
            datafile = "%s/crush/%s/%s-%s-%s.nii.txt" %(tractographypath,segment,segment,counterpart,method)
            oldcalcsfile = "%s/crush/calcs-%s-%s-%s.json" %(tractographypath,segment,counterpart,method)
                    
            if os.path.isfile(nii):
               os.unlink(nii) 
            
            if os.path.isfile(datafile):
               os.unlink(datafile)
                    
            if os.path.isfile(oldcalcsfile):
               print("Cleanup %s" %(oldcalcsfile))
               os.unlink(oldcalcsfile)             

            print(calcs)
            return calcs

    def nonZeroMean(self,faFile,roiFile):
        
        if os.path.isfile(faFile) == False:        
            print("%s is MISSING" %(faFile))
            return
        if os.path.isfile(roiFile) == False:        
            print("%s is MISSING" %(roiFile))
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
            #print(mean)        
        return mean
    def nonZeroStdDev(self,faFile,roiFile):
        
        if os.path.isfile(faFile) == False:        
            print("%s is MISSING" %(faFile))
            return
        if os.path.isfile(roiFile) == False:        
            print("%s is MISSING" %(roiFile))
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
              