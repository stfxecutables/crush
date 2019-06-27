from multiprocessing import Pool,cpu_count
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd
import mglearn
import numpy as np
from scipy import stats
import os,sys
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl


mpl.use('Agg')

results={}
_OUTPUTPATH="."
def f(s,c,m,x):
    try:
       
     if not os.path.isdir("%s/%s" % (_OUTPUTPATH,s)):
        os.mkdir("%s/%s" % (_OUTPUTPATH,s))

     subset1 =df[ (df['ROI Label']==int(s)) & (df['ROI END Label']==int(c)) & (df['Method']==m)]



     allvals = subset1[x].notna()
     nonzero_measures =subset1[allvals].copy()     

     plt.figure()
     genders = ['Male','Female']
    
     for gender in genders:
         subset = nonzero_measures[nonzero_measures['Gender'] == gender]
         if (subset.shape[0]>0):
            #print("s=%s,c=%s,m=%s,x=%s, shape=%s" %(s,c,m,x,subset.shape[0]))
            sns.distplot(subset[x], hist = False, kde = True, ######    TODO
                        kde_kws = {'linewidth': 3},
                        label = gender)
        
        #     # Plot formatting
            plt.legend(prop={'size': 10}, title = 'Gender')
            plt.title('Density Plot per Gender')
            plt.xlabel(x)                           ####################   TODO
            plt.ylabel('Density')
            plt.savefig("%s/%s/%s-%s-%s-%s-Density-Plot.png" %(_OUTPUTPATH,s,s,c,m,x))

     plt.close()

#        print(subset['meanFA'])
#        males = subset[ (subset['Gender']=='Male')]
#        females=subset[ (subset['Gender']=='Female')]

#        male_measures = males[[x]].copy().notna()
#        female_measures = females[[x]].copy().notna()
#        all_measures =subset[[x]].copy().notna()

       
#        if not os.path.isdir("%s/%s" % (_OUTPUTPATH,s)):
#                         os.mkdir("%s/%s" % (_OUTPUTPATH,s))

#        plt.figure()
#        sns.distplot(male_measures, hist = False, kde = True, ######    TODO
#                     kde_kws = {'linewidth': 3},
#                     label = "Male")
#        sns.distplot(female_measures, hist = False, kde = True, ######    TODO
#                     kde_kws = {'linewidth': 3},
#                     label = "Female")            
#        # Plot formatting
#        plt.legend(prop={'size': 10}, title = 'Gender')
#        plt.title('Density Plot per Gender')
#        plt.xlabel(x)                           ####################   TODO
#        plt.ylabel('Density')
#        plt.savefig("%s/%s/%s-%s-%s-%s-Density-Plot.png" %(_OUTPUTPATH,s,s,c,m,x))
#        plt.close()

# #       mmean = male_measures[x].mean()
# #       fmean = female_measures[x].mean()
      
# #       std = all_measures[x].std()
# #       print("male mean:%s female mean:%s std:%s" %(mmean,fmean,std))
# #       d = (mmean - fmean)/std
       
# #       ret = "%s-%s-%s-%s=%s,%s,%s,%s" %(s,c,m,x,mmean,fmean,std,d)
       
    except Exception as err:
        print("%s :: s=%s,c=%s,m=%s,x=%s" %(err,s,c,m,x))
    return ret
    
def storeCorr(result):
    x=result.split('=')
    key=x[0]
    val=x[1]
    results[key]=val
    

    
    

if __name__=="__main__":
    
    #_DATAFILE='/media/dmattie/GENERAL/2019-06-07.small.csv'
    
    #_DATAFILE='~/projects/full.csv'
    #_DATAFILE='~/projects/G0B.csv'
    _DATAFILE = sys.argv[1]
    _OUTPUTPATH=sys.argv[2]
    print("Parsing file %s,rendering to %s" %(_DATAFILE,_OUTPUTPATH))
    
    df = pd.read_csv(_DATAFILE)#.replace(np.nan, 0, regex=True) #nrows=30
    #df.to_pickle('/media/dmattie/GENERAL/2019-06-07.mid.csv.pk')
    #df.to_pickle('/mnt/d/PROJECTS/2019-06-07.mid.csv.pk')
    #df = pd.read_pickle('/media/dmattie/GENERAL/2019-06-07.mid.csv.pk')

    print("Looking for intersections")
    #IntersectionsDF=df[['ROI','ROI END','Method']].drop_duplicates()
    
    #       ['ctx-lh-parahippocampa','ctx-lh-rostralanteriorcingulate','roi_end'],
    #   ['ctx-rh-pericalcarine','wm-lh-temporalpole','roi_end'],
    #   ['Left-Cerebellum-White-Matter','CC_Posterior','roi_end'],
    #   ['Right-vessel','ctx-rh-entorhinal','roi_end'],
    #   ['ctx-lh-superiorfrontal','wm-rh-middletemporal','roi_end'],      
    #   ]
 
    InterestingMeanFA = pd.DataFrame({'ROI Label':['Right-vessel','ctx-lh-superiorfrontal','ctx-rh-caudalanteriorcingulate','ctx-lh-pericalcarine','CC_Anterior','Right-Amygdala','CSF','Left-Amygdala','wm-lh-supramarginal','ctx-rh-precuneus','ctx-lh-parsopercularis','wm-rh-cuneus','wm-lh-inferiortemporal','Right-vessel','CC_Central','ctx-lh-cuneus','ctx-rh-precentral','ctx-rh-fusiform','ctx-lh-bankssts','Left-Cerebellum-White-Matter','ctx-rh-pericalcarine','ctx-lh-parahippocampal',],
                                        'ROI END Label':['ctx-rh-entorhinal','wm-rh-middletemporal','ctx-rh-middletemporal','ctx-lh-precentral','wm-rh-precentral','ctx-lh-precentral','ctx-rh-transversetemporal','wm-rh-middletemporal','wm-rh-parsopercularis','wm-lh-parsopercularis','ctx-rh-pericalcarine','wm-rh-transversetemporal','wm-rh-temporalpole','wm-rh-parsopercularis','wm-lh-parsopercularis','wm-lh-supramarginal','wm-rh-cuneus','wm-lh-postcentral','ctx-rh-postcentral','CC_Posterior','wm-lh-temporalpole','ctx-lh-rostralanteriorcingulate',],
                                        'Method':['roi_end','roi_end','roi','roi_end','roi_end','roi_end','roi','roi_end','roi_end','roi_end','roi','roi_end','roi_end','roi_end','roi_end','roi_end','roi_end','roi_end','roi','roi_end','roi_end','roi_end',]})
	
    IntersectionsDF=pd.DataFrame({'ROI':[51,13,18,255,2018,1016,2021,7,62,1028,2018],
                                  'ROI END':[3019,2022,44,1011,1023,1026,3033,251,2006,4015,2023],
                                  'Method':['roi_end','roi_end','roi_end','roi_end','roi','roi_end','roi_end','roi','roi_end','roi_end','roi_end']})
    #IntersectionsDF=pd.DataFrame({'ROI':[1016],
    #                              'ROI END':[1026],
    #                              'Method':['roi_end']})
    
    Measures=['NumTracts','TractsToRender','LinesToRender','MeanTractLen',
    'MeanTractLen_StdDev','VoxelSizeX','VoxelSizeY','VoxelSizeZ','meanFA',
    'stddevFA','meanADC','stddevADC','NumTracts-asymidx',
    'TractsToRender-asymidx','LinesToRender-asymidx','MeanTractLen-asymidx',
    'MeanTractLen_StdDev-asymidx','VoxelSizeX-asymidx','VoxelSizeY-asymidx',
    'VoxelSizeZ-asymidx','meanFA-asymidx','stddevFA-asymidx',
    'meanADC-asymidx','stddevADC-asymidx']
    
    #Measures=['meanFA']
  
    no_of_procs = cpu_count() -1  #leave 1 core open to keep OS usable
    myPool = Pool(no_of_procs)
    
    print("Pooling out to %s processors to calculate correlation" %(no_of_procs))

    tasks = []
    
    for index, intersection in InterestingMeanFA.iterrows():#IntersectionsDF.iterrows():
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
 