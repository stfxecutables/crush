import sys,os,os.path
import pandas as pd
import matplotlib
import numpy as np
import scipy as sp
import IPython
import sklearn
import argparse
import csv
import mglearn


from sklearn.datasets import load_iris

#from np import genfromtxt

class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file hand

def main():    
    parser = argparse.ArgumentParser(
        description='ML for Crush is used to iterrogate data extracted from.')
    
    parser.add_argument('-i', dest="file",required=True,
                        help="Path to data file",
                        metavar="FILE",
                        type=lambda x: is_valid_file(parser,x))
                        
     

    args = parser.parse_args()
    
    ## Build crushdata from file
    dataset={}
    with open(args.file.name) as fin:
        reader=csv.reader(fin, skipinitialspace=True, quotechar="'")
        for row in reader:
            dataset[row[0]]=row[:]  
            exit
    dataArray = np.genfromtxt(args.file.name, delimiter=',', skip_header=1)#,                  usecols=range(2,32))
    crushdata = Bunch(feature_names=dataset['VisitID'],data=dataArray)
    
    print("%s features, %s samples" % (len(crushdata.feature_names),len(crushdata.data)))

    #print(crushdata.feature_names)
    crush_dataframe = pd.DataFrame(crushdata.data, columns=crushdata.feature_names)

    ts = pd.plotting.scatter_matrix(crush_dataframe,marker='0',hist_kwds={'bins':20},s=60,alpha=0.8, cmap=mglearn.cm3)
    ts.plot()
    pd.tseries.plotting.pylab.show()

    ##
    
    #print("Keys of dataset:\n{}".format(data.keys()))

    #print(data['VisitID'][:4])
    #print(dataArray.shape)
    ##IRIS

    #iris_dataset = load_iris()
    #print("Keys of IRIS Dataset: \n{}".format(iris_dataset.keys()))
    #print("Target names: {}".format(iris_dataset['target_names']))
    #print("shape of data: {}".format(iris_dataset['data'].shape))


if __name__ == '__main__':
    main()
