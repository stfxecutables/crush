import sys,os,os.path
import argparse
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd
import mglearn
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.impute import SimpleImputer

from pandas.compat import StringIO, BytesIO

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

    parser.add_argument('-method',action='store',
                        help='Specify learning method to invoke: [knn,pca,guided]') 

    parser.add_argument('-focus', dest="focus",required=True,
                        help="A csv file representing tracts to manually narrow dataset. one line per tract.  e.g. ctx-lh-insula,wm-lh-lateraloccipital,roi_end",
                        metavar="FILE",
                        type=lambda x: is_valid_file(parser,x))
                        
    args = parser.parse_args()  

    if args.method == "knn":
        knnMethod(args)
    elif args.method =="pca":
        pcaMethod(args)
    elif args.method =="guided":
        guidedMethod(args)
    else:
        print("all")
    #pcaMethod(args)

def guidedMethod(args):
    #--GUIDED manually via -mostcorrelated switch
    datafile = "%s.pk" %(args.file.name)
    if os.path.isfile(datafile):
        df = pd.read_pickle(datafile)
    else:
        df = pd.read_csv(args.file.name)
    #df.to_pickle("%s.pk" %(args.file.name))

    focus={}

    if os.path.isfile(args.focus.name):
        with open(args.focus.name) as f:
            for line in f:
                focus[line.rstrip()]=True
    else:
        print("To use guided method, -focus must be used")
        return

    
    good_bye_list = []
    for column in df:
        if column !="Age" and column != "PatientId" and column != "VisitId" and column !="Gender":
            if column not in focus:
                good_bye_list.append(column)

    df.drop(good_bye_list,axis=1,inplace=True)
    
    target = df[['Gender']]
    features = df.iloc[:,3:]

    features_nona = features.copy()
    features_nona.fillna(features_nona.mean(),inplace=True)   
    features_nona=features_nona.dropna(axis=1,how='all')


    
    X_train,X_test,y_train,y_test=train_test_split(features_nona,target,random_state=0)
    print("X_train shape: {}".format(X_train.shape))
    print("y_train shape: {}".format(y_train.shape))
    print("X_test shape: {}".format(X_test.shape))
    print("y_test shape: {}".format(y_test.shape))

    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier(n_neighbors=1)

    knn.fit(X_train,y_train.values.ravel())

    X_test=X_test.copy()    
    X_test.fillna(X_train.mean(),inplace=True)

    y_pred = knn.predict(X_test)

    print("KNN Test set predictions:\n {}".format(y_pred))
    print("KNN Test set tests:\n {}".format(y_test))
    #print("test set score: {:.2f}".format(np.mean(y_pred == y_test.values.tolist())))   
    print("KNN test set score: {:.2f}".format(knn.score(X_test,y_test)))
    

def knnMethod(args):
    #-- KNN ------17819459-------------------------------------------------------

   # args = parser.parse_args()        
    df = pd.read_csv(args.file.name).replace(np.nan, 0, regex=True) #nrows=30
    target = df[['Gender']]
    features = df.iloc[:,3:]

    X_train,X_test,y_train,y_test=train_test_split(features,target,random_state=0)
    print("X_train shape: {}".format(X_train.shape))
    print("y_train shape: {}".format(y_train.shape))
    print("X_test shape: {}".format(X_test.shape))
    print("y_test shape: {}".format(y_test.shape))


    #pd.plotting.scatter_matrix(features,figsize=(15,15),marker='o',hist_kwds={'bins':20},s=60,alpha=.8,cmap=mglearn.cm3)
    #plt.show()

    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X_train,y_train.values.ravel())

    y_pred = knn.predict(X_test)
    #print(y_pred)
    #print(y_test)
    print("KNN Test set predictions:\n {}".format(y_pred))
    print("KNN Test set tests:\n {}".format(y_test))
    #print("test set score: {:.2f}".format(np.mean(y_pred == y_test.values.tolist())))   
    print("KNN test set score: {:.2f}".format(knn.score(X_test,y_test)))

def pcaMethod(args):
    #-- PCA ----------------------------------------------------------------------

         
    df = pd.read_csv(args.file.name).replace(np.nan, 0, regex=True) #nrows=30
    target = df[['Gender']]
    features = df.iloc[:,3:]

    X_train,X_test,y_train,y_test=train_test_split(features,target,random_state=0)
    print("X_train shape: {}".format(X_train.shape))
    print("y_train shape: {}".format(y_train.shape))
    print("X_test shape: {}".format(X_test.shape))
    print("y_test shape: {}".format(y_test.shape))

    components = 100
    if components>X_train.ndim:
        components=X_train.ndim
    pca = PCA(n_components = components,whiten=True,random_state=0).fit(X_train) 
    X_train_pca = pca.transform(X_train)
    X_test_pca = pca.transform(X_test)

    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X_train_pca,y_train.values.ravel())

    print("Test set accuracy: {:.2f}".format(knn.score(X_test_pca,y_test)))



if __name__ == '__main__':
    main()
