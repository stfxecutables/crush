import os, sys
#from pathlib import Path
from patient import Patient

class Samples:
    Count=0
    
    def __init__(self,rootDir):
        self.Patients=[]
        print("Initializing Patients")

        dirs = os.listdir( rootDir )
        
        for file in dirs:
           
            patient_dir = "%s/%s" % (rootDir,file)
            visit_dir = "%s/%s/01" % (rootDir,file)
            if os.path.exists(visit_dir): #assume if at least one visit then patient
                self.Count+=1
                patient=Patient(patient_dir)
                self.Patients.append(patient)

                
