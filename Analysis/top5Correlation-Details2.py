from multiprocessing import Pool,cpu_count
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import Math, Latex
# for displaying images
from IPython.core.display import Image

import sys,os,os.path
import argparse
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd
import mglearn
import numpy as np
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier

from pandas.compat import StringIO, BytesIO
import matplotlib as mpl
mpl.use('Agg')

# settings for seaborn plotting style
sns.set(color_codes=True)
# settings for seaborn plot sizes
sns.set(rc={'figure.figsize':(5,5)})


from scipy.stats import uniform



results={}
_OUTPUTPATH="."

def f(s,c,m,x):
    try:
       
        if not os.path.isdir("%s/%s_%s_%s" % (_OUTPUTPATH,s,c,m)):
            os.mkdir("%s/%s_%s_%s" % (_OUTPUTPATH,s,c,m))
        
        subset1 =df[ (df['ROI Label']==s) & (df['ROI END Label']==c) & (df['Method']==m)]

        #print(subset1)

        allvals = subset1[x].notna()
        nonzero_measures =subset1[allvals].copy()  

        nonzero_measures_x = nonzero_measures[[
                'Age', 
                #'Gender',      
                x
                ]]   
        
        plt.figure()
        
        sns.regplot('Age',x,nonzero_measures_x)
        
        fa=("%s/%s_%s_%s/%s-regplot.png" %(_OUTPUTPATH,s,c,m,x))
        
        plt.title('Changes in log age vs log NumTracts')
        plt.xlabel('Age')                           ####################   TODO
        plt.ylabel(x)        
        plt.savefig(fa)
       
        plt.figure()
        
        sns.pairplot(nonzero_measures_x,diag_kind='auto',plot_kws={'alpha':0.2})        
        fc=("%s/%s_%s_%s/%s-pairplot.png" %(_OUTPUTPATH,s,c,m,x))
        plt.savefig(fc)






    except Exception as err:
        print("%s :: s=%s,c=%s,m=%s,x=%s" %(err,s,c,m,x))
    return ret

    
def storeCorr(result):
    x=result.split('=')
    key=x[0]
    val=x[1]
    results[key]=val
    
if __name__=="__main__":    


    _DATAFILE=sys.argv[1]
    _OUTPUTPATH = sys.argv[2]
    _INTERESTINGCSV=sys.argv[3]

    print("Parsing file %s,rendering to %s" %(_DATAFILE,_OUTPUTPATH))

    df = pd.read_csv(_DATAFILE)#.replace(np.nan, 0, regex=True) #nrows=30

    InterestingROI = pd.read_csv(_INTERESTINGCSV)

    Measures=['NumTracts','TractsToRender','LinesToRender','MeanTractLen',
    'MeanTractLen_StdDev','VoxelSizeX','VoxelSizeY','VoxelSizeZ','meanFA',
    'stddevFA','meanADC','stddevADC','NumTracts-asymidx',
    'TractsToRender-asymidx','LinesToRender-asymidx','MeanTractLen-asymidx',
    'MeanTractLen_StdDev-asymidx','VoxelSizeX-asymidx','VoxelSizeY-asymidx',
    'VoxelSizeZ-asymidx','meanFA-asymidx','stddevFA-asymidx',
    'meanADC-asymidx','stddevADC-asymidx']

    no_of_procs = cpu_count() -1  #leave 1 core open to keep OS usable
    myPool = Pool(no_of_procs)

    print("Pooling out to %s processors to calculate correlation" %(no_of_procs))

    tasks = []

    for index, intersection in InterestingROI.iterrows():#IntersectionsDF.iterrows():
        roi=str(intersection['ROI Label'])#.zfill(4)
        roiEnd=str(intersection['ROI END Label'])#.zfill(4)
        method=intersection['Method']
        
        for measure in Measures:
            tasks.append([roi,roiEnd,method,measure])
    for t in tasks:
    #    print(t)
        r= myPool.apply_async(f,args=(t[0],t[1],t[2],t[3],),callback=storeCorr)

    print("Submitted tasks to pool")

    myPool.close()
    myPool.join()
    for k in results:
        print("%s,%s" %(k,results[k]))
 