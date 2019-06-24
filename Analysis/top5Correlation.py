from multiprocessing import Pool,cpu_count
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd
import mglearn
import numpy as np
from scipy import stats


results={}
def f(s,c,m,x):
    try:
       subset = df[ (df['ROI']==int(s)) & (df['ROI END']==int(c)) & (df['Method']==m)]
       supersubset = subset[['Age',x]].copy()
       ss = supersubset[supersubset[x].notna()]
       corr = ss['Age'].corr(ss[x])
       #x, y = ss['Age'].values, ss[x].values
       #print(ss[x])
       #print(ss.notna())
       pearson_coef, p_value = stats.pearsonr( ss['Age'].values,ss[x].values)
       ret = "%s-%s-%s-%s=%s,%s,%s" %(s,c,m,x,corr,pearson_coef,p_value)
       
    except Exception as err:
        print(err)
    return ret
    
def storeCorr(result):
    x=result.split('=')
    key=x[0]
    val=x[1]
    results[key]=val
    

    
    

if __name__=="__main__":
    
    #_DATAFILE='/media/dmattie/GENERAL/2019-06-07.small.csv'
    _DATAFILE='~/projects/full.csv'
    #_DATAFILE='~/projects/G0B.csv'
    print("Parsing file %s" %(_DATAFILE))
    
    df = pd.read_csv(_DATAFILE)#.replace(np.nan, 0, regex=True) #nrows=30
    #df.to_pickle('/mnt/d/PROJECTS/2019-06-07.mid.csv.pk')
    #df = pd.read_pickle('/mnt/d/PROJECTS/2019-06-07.mid.csv.pk')

    print("Looking for intersections")
    IntersectionsDF=df[['ROI','ROI END','Method']].drop_duplicates()
    
    #IntersectionsDF=pd.DataFrame({'ROI':[2,4,1028],
    #                              'ROI END':[4,2,3028],
    #                              'Method':['roi','roi_end','roi']})
    #IntersectionsDF=pd.DataFrame({'ROI':[1028],
    #                              'ROI END':[3028],
    #                              'Method':['roi']})
    
    Measures=['NumTracts','TractsToRender','LinesToRender','MeanTractLen',
    'MeanTractLen_StdDev','VoxelSizeX','VoxelSizeY','VoxelSizeZ','meanFA',
    'stddevFA','meanADC','stddevADC','NumTracts-asymidx',
    'TractsToRender-asymidx','LinesToRender-asymidx','MeanTractLen-asymidx',
    'MeanTractLen_StdDev-asymidx','VoxelSizeX-asymidx','VoxelSizeY-asymidx',
    'VoxelSizeZ-asymidx','meanFA-asymidx','stddevFA-asymidx',
    'meanADC-asymidx','stddevADC-asymidx']
    #Measures=['NumTracts']
  
    no_of_procs = cpu_count() -1  #leave 1 core open to keep OS usable
    myPool = Pool(no_of_procs)
    
    print("Pooling out to %s processors to calculate correlation" %(no_of_procs))

    tasks = []
    
    for index, intersection in IntersectionsDF.iterrows():
        roi=str(intersection['ROI'])#.zfill(4)
        roiEnd=str(intersection['ROI END'])#.zfill(4)
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
 
#import os, sys,inspect
#from multiprocessing import Pool,cpu_count
##!/usr/bin/env python3
#def f(parr):
#  
#    segment=parr[0]
#    counterpart=parr[1]
#    method=parr[2]
#
#    print("Processing: %s-%s-%s" %'NumTracts'(segment,counterpart,method))
#    
#def trackvis_worker(self,parr):#segment,counterpart,method):
#    print("X")
#    segment=parr[0]
#    counterpart=parr[1]
#    method=parr[2]
#
#    print("Processing: %s-%s-%s" %(segment,counterpart,method))
#      
#    
#    #return x*x
#def main():  
#    pool = Pool(processes=4)              # start 4 worker processes
#    
#    tasks = []
#    tasks.append( ["3028","1028","roi"] )
#    tasks.append( ["1028","3028","roi_end"] )
#    print(tasks)
#    no_of_procs = cpu_count() 
#    pool = Pool(no_of_procs)
#    for t in tasks:
#        pool.apply_async(trackvis_worker, (t,))            
#    pool.close()
#    pool.join()
#    
#
#
#if __name__ == '__main__':
#    main()
#
#
