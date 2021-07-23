from multiprocessing import Pool,cpu_count
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd
import mglearn
import numpy as np


results={}
def f(s,c,m):
    ret = "%s-%s-%s=1" %(s,c,m)
    print(ret)
    return ret
    try:
        
      
            
       subset = df[ (df['ROI']==int(s)) & (df['ROI END']==int(c)) & (df['Method']==m)]
       
       print(subset.shape)
       
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
    #_DATAFILE='/media/dmattie/crush/2019-06-07.tiny.csv'
    _DATAFILE='/media/dmattie/crush/fiftyk.csv'
    df = pd.read_csv(_DATAFILE).replace(np.nan, 0, regex=True) #nrows=30
    IntersectionsDF=df[['ROI','ROI END','Method']].drop_duplicates()
    
    
     

    no_of_procs = cpu_count() -1  #leave 1 core open to keep OS usable
    myPool = Pool(no_of_procs)

    tasks = []
    
    for index, intersection in IntersectionsDF.iterrows():
        roi=str(intersection['ROI'])#.zfill(4)
        roiEnd=str(intersection['ROI END'])#.zfill(4)
        method=intersection['Method']
        tasks.append([roi,roiEnd,method])

    
    for t in tasks:
        r= myPool.apply_async(f,args=(t[0],t[1],t[2],),callback=storeCorr)
       

    print("Submitted tasks to pool")

    myPool.close()
    myPool.join()
    #print(results)
 
#import os, sys,inspect
#from multiprocessing import Pool,cpu_count
##!/usr/bin/env python3
#def f(parr):
#  
#    segment=parr[0]
#    counterpart=parr[1]
#    method=parr[2]
#
#    print("Processing: %s-%s-%s" %(segment,counterpart,method))
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
