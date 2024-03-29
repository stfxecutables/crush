import os, sys,inspect
import subprocess
#from pathlib import Path
from basecrush.ux import MsgUser
from basecrush.visit import Visit

    
class Patient:
    
    def __init__(self,path,rebuild,voi,recrush,fixmissing,maxcores,disable_log,pipeline,gradienttable,b0):        
        self.PatientId=os.path.basename(path)
        self.rebuild=rebuild
        self.voi=voi
        self.recrush=recrush
        self.fixmissing=fixmissing
        self.maxcores=maxcores
        self.disable_log=disable_log
        self.pipeline=pipeline
        self.gradienttable=gradienttable
        self.b0=b0
        
        self.Visits=[]
        
        visits = os.listdir( path )
        
        for v in visits:
            visitPathTest="%s/%s/Freesurfer/mri" % (path,v)
            
            if os.path.exists(visitPathTest) and v!="fsaverage":
                
                visitPath="%s/%s" %(path,v)
                thisVisit = Visit(visitPath,self.rebuild,voi,recrush,fixmissing,maxcores,self.disable_log,self.pipeline,self.gradienttable,self.b0)
                self.Visits.append(thisVisit)
            else: #cases where there is only one visit, like HCP
                visitPathTest="%s/%s/%s/mri" % (path,v,self.PatientId)
            
                if os.path.exists(visitPathTest) and v!="fsaverage":
                    visitPath="%s/%s" %(path,v)
                    thisVisit = Visit(visitPath,self.rebuild,voi,recrush,fixmissing,maxcores,self.disable_log,self.pipeline,self.gradienttable,self.b0)
                    self.Visits.append(thisVisit)

    