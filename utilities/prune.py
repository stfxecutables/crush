import sys,os,os.path
import argparse
import pandas as pd
import numpy as np


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file hand


def main():    
    parser = argparse.ArgumentParser(
        description='A utility to prune a csv and extract specific columns identified in -focus.')
    
    parser.add_argument('-i', dest="file",required=True,
                        help="Path to CSV file",
                        metavar="FILE",
                        type=lambda x: is_valid_file(parser,x))

    parser.add_argument('-focus', dest="focus",required=True,
                        help="A text file representing column headers to extract from CSV. one line per header.",
                        metavar="FILE",
                        type=lambda x: is_valid_file(parser,x))

    args = parser.parse_args()

    datafile = "%s.pk" %(args.file.name)  
    if os.path.isfile(datafile):
        df = pd.read_pickle(datafile)
    else:
        df = pd.read_csv(args.file.name)  
    
    focus={}
    with open(args.focus.name) as f:
        for line in f:
            focus[line.rstrip()]=True

    
    good_bye_list = []
    for column in df:
        
        if column not in focus:
            #print(column)
            good_bye_list.append(column)
               
    #print("Shape of good_bye_list: {}".format(good_bye_list.shape))
    df.drop(good_bye_list,axis=1,inplace=True)
    #print("Shape of df: {}".format(df.shape))
    print(df.to_csv())


if __name__ == '__main__':
    main()
                          