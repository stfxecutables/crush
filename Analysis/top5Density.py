from multiprocessing import Pool,cpu_count
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd
import mglearn
import numpy as np
from scipy import stats
import sys
import time

results={}
progress=[False for i in range(101)]
tasklen=0

def f(s,c,m,x):
    try:
       subset = df[ (df['ROI']==int(s)) & (df['ROI END']==int(c)) & (df['Method']==m)]

       males = subset[ (subset['Gender']=='Male')]
       females=subset[ (subset['Gender']=='Female')]

       male_measures = males[[x]].copy().notna()
       female_measures = females[[x]].copy().notna()
       all_measures =subset[[x]].copy().notna()

       mmean = male_measures[x].mean()
       fmean = female_measures[x].mean()
      
       std = all_measures[x].std()
       #print("male mean:%s female mean:%s std:%s" %(mmean,fmean,std))
       if(std>0):
           d = (mmean - fmean)/std
       else:
           d = ""
       
       ret = "%s-%s-%s-%s=%s,%s,%s,%s" %(s,c,m,x,mmean,fmean,std,d)
       
    except Exception as err:
        print(err)
    return ret
    
def storeCorr(result):
    global counter
    global tasklen
    x=result.split('=')
    key=x[0]
    val=x[1]
    results[key]=val
    counter = counter+1
    prog =int((counter/tasklen)*100)
    
    
    if(prog>0 and prog<=100):
        if prog not in progress:
            progress[prog]=True
        else:
            print("%s \% complete" %(prog))
        

    
    

if __name__=="__main__":
    
    #_DATAFILE='/media/dmattie/GENERAL/2019-06-07.small.csv'
    
    #_DATAFILE='~/projects/full.csv'
    #_DATAFILE='~/projects/G0B.csv'
    _DATAFILE = sys.argv[1]
    counter=0
    print("Parsing file %s" %(_DATAFILE))
    
    #df = pd.read_csv(_DATAFILE)#.replace(np.nan, 0, regex=True) #nrows=30
    #df.to_pickle('/media/dmattie/GENERAL/2019-06-07.mid.csv.pk')
    #df.to_pickle('/mnt/d/PROJECTS/2019-06-07.mid.csv.pk')
    df = pd.read_pickle('/media/dmattie/GENERAL/2019-06-07.mid.csv.pk')

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
    tasklen=len(tasks)
    print("Number of tasks: %s" %(tasklen))
    for t in tasks:
    #    print(t)
        r= myPool.apply_async(f,args=(t[0],t[1],t[2],t[3],),callback=storeCorr)

    print("Submitted tasks to pool")

    myPool.close()
    myPool.join()
    print("Results calculated")
    for k in results:
        print("%s,%s" %(k,results[k]))
 