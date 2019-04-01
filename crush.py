import os, sys, argparse,re
from tractcrush.samples import Samples
from tractcrush.ux import MsgUser
import numpy


class readable_dir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values
        if not os.path.isdir(prospective_dir):
            MsgUser.failed("-samples path ({0}) is not a valid path".format(prospective_dir))
            exit(1)
            #raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(prospective_dir))
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace, self.dest, prospective_dir)
        else:
            MsgUser.failed("-samples path ({0}) is not a readable dir".format(prospective_dir))
            exit(1)
            #raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))


def VersionCheck():
    fsFile = "%s/build-stamp.txt" % (os.environ['FREESURFER_HOME'])

    if os.path.isfile(fsFile) == False:
        MsgUser.failed("FreeSurfer is MISSING (%s)" % (fsFile))

    with open(fsFile, "r") as f:
        fsv_content = f.readlines()

        m = re.search(r'freesurfer-.*-stable-pub-(\w+)', fsv_content[0])  # -[a-zA-Z0-9]{7}
        if m:
            fsversion = m.group(1).strip()
            if fsversion == "v6":
                MsgUser.ok("Freesurfer Version v6 detected and supported")
                
            else:
                MsgUser.warning("Freesurfer Version %s detected.  CRUSH wasn't tested with this version" % fsversion)
        else:
            MsgUser.warning("Unable to determine valid FreeSurfer version in file (%s)" % fsFile)

def StatusReport(args,S):
    l_v = 0
    print("Sample size:%i" % (len(S.Patients)))
    for p in S.Patients:
        if (args.patient is not None and args.patient != p.PatientId):
            continue
        l_v += len(p.Visits)

    for p in S.Patients:
        if (args.patient is not None and args.patient != p.PatientId):
            continue
        for v in p.Visits:            
            if v.ReconComplete:
                l_reconall_message = "Cortical Reconstruction Complete"
            else:                
                l_reconall_message = "Cortical Reconstruction INCOMPLETE"

            if not v.ReconComplete:
                l_parcellation_message = "NOT Parcellated"
            else:
                l_parcellation_message = "Parcellated"

            if not v.MeasurementComplete:
                l_measurement_message = "NO Measurements"
            else:
                l_measurement_message = "Measurement Complete"

        print("%s/%s %s, %s, %s" % (
            p.PatientId, len(p.Visits), l_reconall_message, l_parcellation_message, l_measurement_message))

def ProcessSamples(args,S):
    print("no render")
    for p in S.Patients:
        if (args.patient is not None and args.patient != p.PatientId):
            continue
        for v in p.Visits:

            if v.ReconComplete != True:
                MsgUser.warning("\t%s recon incomplete" % (v.VisitId))
            else:
                v.Render()
                v.Measure()
def main():                

    ldir = "."
    parser = argparse.ArgumentParser(
        description='Connectomics and Reporting User Shell is used to iterrogate samples, generate or extract measurements.')
    parser.add_argument('-samples', action=readable_dir, default=ldir, help="Path to patient samples")
    parser.add_argument('-status', action="store_true", help="Report back what is out there and what needs to be done")
    parser.add_argument('-recon', action='store_true', help='Apply recon-all for any T1.mgz found beneath working folder')
    parser.add_argument('-norender', action='store_true', default='n',
                        help='If there are incomplete connectomes, ignore the outstanding work')
    parser.add_argument('-rebuild', action='store_true',
                        help='Recreate any intermediary files used for establishing measurements.  If this not specified, any intermetiate files found with the appriate file name will be left untouched.')
    parser.add_argument('-patient', action='store',
                        help='Specify patient ID of interest if focusing on a single patient')
    parser.add_argument('-voi', action='store',
                        help='Values of Interest - Path to text file that lists values of interest to extract.  One column per line.  Look at any patient sample tractography\\crush\\tracts.txt file for measures.')
    parser.add_argument('-recrush',action='store_true',
                        help='Ignore anything previosly crushed and re-extract tract information')
    parser.add_argument('-fixmissing',action='store_true',
                        help='Ignore anything previosly crushed and extract only tract information that has not been rendered yet')                        
    parser.add_argument('-report',action='store_true',
                        help='Extract a row-based table for analysis, 1 row per measure')  
    parser.add_argument('-columnar',action='store_true',
                        help='Extract a column-based table for analysis, 1 row per patient')                         
    parser.add_argument('-metadata',action='store',
                        help='Path to metadata file about patient.  The metadata file should have the CSV format Patient,Visit,Attr1..AttrN')                                               
    args = parser.parse_args()

    S = Samples(args.samples, args.rebuild, args.voi, args.recrush,args.metadata,args.fixmissing)

    if (args.report):
        S.Report()        
        exit()
    if (args.columnar):
        S.Columnar()
        exit()        
    # Read VOI into array
    if (args.voi):

        if os.path.isfile("%s" % (args.voi)):
            # Print Header
            row=[]
            row.append("PatientID")
            row.append("VisitID")
            with open(args.voi) as f:
                content = f.readlines()
                content = [x.strip() for x in content]  # Remove Whitespace
                for c in content:
                    row.append(c)
                print(",".join(row))

            for p in S.Patients:
                if (args.patient is not None and args.patient != p.PatientId):
                    continue
                # Print values from each patient visit
                for v in p.Visits:
                    v.Report2()  
                    #print(v.data)                  
        else:
            print("voi file not found (%s)" % (args.voi))


    else:
        VersionCheck()
        print("\n################## CRUSH ##################")
        print("#  Connectomics and Reporting User Shell  #")
        print("###########################################\n")
        if S.Patients is None:
            print("No patient samples found in path [%s].  Specify -samples for alternate path." % (args.samples))
        else:        
            # STATUS REPORT ############################################################
            
            if (args.status):
                StatusReport(args,S)
                
            
            # RENDER ANYTHING OUTSTANDING ##############################################
            if ((args.status is None or args.status==False) and (args.norender is None or args.norender != 'y')):
                ProcessSamples(args,S)

        MsgUser.ok("We are done")


if __name__ == '__main__':
    main()

