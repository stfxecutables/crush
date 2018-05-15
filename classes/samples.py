import os, sys
#from pathlib import Path
from patient import Patient

class Samples:
    Count=0
    
    def __init__(self,rootDir,force,voi):
        self.Patients=[]
        self.force=force
        self.voi=voi

        dirs = os.listdir( rootDir )
        
        for file in dirs:
           
            patient_dir = "%s/%s" % (rootDir,file)
            if os.path.isdir(patient_dir):
                visits = os.listdir(patient_dir)
                for v in visits:
                    if(not os.path.islink("%s/%s" %(patient_dir,v))):
                        mri_dir = "%s/%s/mri" % (patient_dir,v)
                        if os.path.exists(mri_dir):
                            #print "%s/%s/mri" %(patient_dir,v)
                            #visit_dir = "%s/%s/01" % (rootDir,file)
                            #if os.path.exists(visit_dir): #assume if at least one visit then patient
                            self.Count+=1
                            patient=Patient(patient_dir,self.force,self.voi)
                            self.Patients.append(patient)


