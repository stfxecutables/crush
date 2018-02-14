import os, sys,inspect
import subprocess
#from pathlib import Path
from ux import MsgUser
from visit import Visit

    
class Patient:

    def __init__(self,path):
        self.Id=os.path.basename(path)
        
        self.Visits=[]
        
        visits = os.listdir( path )
        
        for v in visits:
            visitPathTest="%s/%s/mri" % (path,v)
            
            if os.path.exists(visitPathTest) and v!="fsaverage":
                
                visitPath="%s/%s" %(path,v)
                thisVisit = Visit(visitPath)
                self.Visits.append(thisVisit)
    