#!/usr/bin/python

import os, sys
from classes.samples import Samples
from classes.ux import MsgUser

rootDir=sys.argv[1]    

S=Samples(rootDir)
print("################## ATLAS ##################")
if S.Patients:
    print("%i patients" % (len(S.Patients)))

#Take stock
for p in S.Patients:
    print("\nPatient:%s, %s mri visit(s)" % (p.Id, len(p.Visits)))
    for v in p.Visits:
        
        if v.ReconComplete != True:
            MsgUser.warning("\t%s recon incomplete" %(v.Id))
        else:
            v.Render()
                
          

            

MsgUser.ok("We are done") 
