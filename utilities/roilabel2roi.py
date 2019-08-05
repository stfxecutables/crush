import sys,os,os.path,inspect,re
import argparse
import csv


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file hand


def main():
    parser = argparse.ArgumentParser(
        description='roilabel2roi accepts a file and writes it back replacing any ROI Label found in ../basecrush/segmentMap.csv with equivalent ROI values.')
    
    parser.add_argument('-i', dest="file",required=True,
                        help="Path to data file",
                        metavar="FILE",
                        type=lambda x: is_valid_file(parser,x))
    
    args = parser.parse_args()  
    Segments = []#{}

    i=1
    segmentMap="%s/../basecrush/%s" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),"segmentMap.csv")
    with open(segmentMap) as fin:
        reader=csv.reader(fin, skipinitialspace=True, quotechar="'")
        p = re.compile('^ *#')   # if not commented          
        for row in reader:
            #print("%s,%s" %(i,row))
            if(i>1 and not p.match(row[0])): 
                Segments.append({'roi':row[0],'roiname':row[1],'asymmetry':row[2]})
            i=i+1
   
    if os.path.isfile(args.file.name):
        with open(args.file.name) as f:
            for line in f:
                l=line.rstrip('\n')
                for s in Segments:
                   #print(s)
                   l=l.replace(s['roiname'],s['roi'],1)
                   
                print(l)
            #lines = [line.rstrip('\n') for line in f]
    #print(lines)                        

if __name__ == '__main__':
    main()
