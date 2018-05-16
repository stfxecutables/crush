#!/usr/bin/python

import os, sys,argparse
from classes.samples import Samples
from classes.ux import MsgUser

class readable_dir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir=values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(prospective_dir))
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace,self.dest,prospective_dir)
        else:
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))

            
            
#rootDir=sys.argv[1] 
ldir="."
parser = argparse.ArgumentParser(description='Iterrogate samples, generate or extract measurements.')
parser.add_argument('-samples', action=readable_dir,default=ldir,help="Path to patient samples")
parser.add_argument('-rebuild', action='store_true',
                    help='Recreate any intermediary files used for establishing measurements')
parser.add_argument('-patient', action='store')
parser.add_argument('-voi',action='store',
                   help='Values of Interest - Path to text file that lists values of interest to extract.  One column per line.')
args = parser.parse_args()

S=Samples(args.samples,args.rebuild,args.voi)

#Read VOI into array
if os.path.isfile("%s" %(args.voi)):
    #Print Header    
    with open(args.voi) as f:
            content = f.readlines()
            content = [x.strip() for x in content] #Remove Whitespace
            print(",".join(content))
            

    for p in S.Patients:
        if (args.patient is not None and args.patient != p.Id):
            continue
        #Print values from each patient visit
        for v in p.Visits:
            v.Report()
            

else:

    print("################## ATLAS ##################")
    if S.Patients:
        print("%i patients" % (len(S.Patients)))

    #Take stock
    for p in S.Patients:
        if (args.patient is not None and args.patient != p.Id):
            continue

        print("\nPatient:%s, %s mri visit(s)" % (p.Id, len(p.Visits)))
        for v in p.Visits:

            if v.ReconComplete != True:
                MsgUser.warning("\t%s recon incomplete" %(v.Id))
            else:
                v.Render()
                v.Measure()





    MsgUser.ok("We are done") 
