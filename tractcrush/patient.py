import os, sys,inspect
import subprocess
#from pathlib import Path
from tractcrush.ux import MsgUser
from tractcrush.visit import Visit

    
class Patient:

    def __init__(self,path,rebuild,voi,recrush,fixmissing,maxcores,disable_log):        
        self.PatientId=os.path.basename(path)
        self.rebuild=rebuild
        self.voi=voi
        self.recrush=recrush
        self.fixmissing=fixmissing
        self.maxcores=maxcores
        self.disable_log=disable_log
        
        self.Visits=[]
        
        visits = os.listdir( path )
        
        for v in visits:
            visitPathTest="%s/%s/Freesurfer/mri" % (path,v)
            
            if os.path.exists(visitPathTest) and v!="fsaverage":
                
                visitPath="%s/%s" %(path,v)
                thisVisit = Visit(visitPath,self.rebuild,voi,recrush,fixmissing,maxcores,self.disable_log)
                self.Visits.append(thisVisit)
    