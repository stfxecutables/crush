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
mpl.rcParams['figure.max_open_warning'] = 0


if __name__=="__main__":
    
    _DATAFILE = sys.argv[1]
    _OUTPUTPATH=sys.argv[2]
    _LEFTLABEL=sys.argv[3]
    _RIGHTLABEL=sys.argv[4]
    _METHOD=sys.argv[5]
    _MEASURE=sys.argv[6]


    if not os.path.isdir(_OUTPUTPATH):
        os.mkdir(_OUTPUTPATH)

    print("Parsing file %s" %(_DATAFILE))
    
    df = pd.read_csv(_DATAFILE)#.replace(np.nan, 0, regex=True) #nrows=30
    #df.to_pickle('/mnt/d/PROJECTS/2019-06-07.mid.csv.pk')
    #df = pd.read_pickle('/media/dmattie/GENERAL/2019-06-07.mid.csv.pk')

    all =df[['Age',_MEASURE]].copy()
    allna=all[all[_MEASURE].notna()]
    pearson_coef, p_value = stats.pearsonr( allna['Age'].values,allna[_MEASURE].values)
    print(pearson_coef,p_value)
       
    subset = df[ (df['ROI Label']==_LEFTLABEL) & (df['ROI END Label']==_RIGHTLABEL) & (df['Method']==_METHOD)]
    supersubset = subset[['Age',_MEASURE]].copy()
    ss = supersubset[supersubset[_MEASURE].notna()]

    df=len(ss.index)       
    pearson_coef, p_value = stats.pearsonr( ss['Age'].values,ss[_MEASURE].values)
    ret = "All %s/%s/%s/%s :: r(%s)=%s,p=%s" %(_LEFTLABEL,_RIGHTLABEL,_METHOD,_MEASURE,df,pearson_coef,p_value)
    print(ret)
    
    plt.figure()
    gM = sns.regplot(x='Age',y=_MEASURE,data=ss,scatter_kws={"color": "blue"}, line_kws={"color": "blue",'label': "r(%s)={0:.3f},p={1:.3f}".format(pearson_coef,p_value)%(df)})
    t = plt.figtext(0.05, 0.95, '%s to %s, %s' %(_LEFTLABEL,_RIGHTLABEL,_METHOD), horizontalalignment='left') 
    t.set_alpha(0.5)
    plt.title('Correlation of %s with Age' %(_MEASURE))
    gM.legend()
    plt.xlabel("Age") 
    plt.ylabel(_MEASURE)

    plt.savefig("%s/%s__%s__%s__%s__correlation.png" %(_OUTPUTPATH,_LEFTLABEL,_RIGHTLABEL,_METHOD,_MEASURE))
    
    plt.close()

    ##### U15

    UNidx=ss.Age<=15
    UN=ss[UNidx]
    dfN=len(UN.index)
     
    pearson_coef, p_value = stats.pearsonr( UN['Age'].values,UN[_MEASURE].values)
    ret = "U15 %s/%s/%s/%s :: r(%s)=%s,p=%s" %(_LEFTLABEL,_RIGHTLABEL,_METHOD,_MEASURE,dfN,pearson_coef,p_value)
    print(ret)

    ##### U10
    UNidx=ss.Age<=10
    UN=ss[UNidx]
    dfN=len(UN.index)
     
    pearson_coef, p_value = stats.pearsonr( UN['Age'].values,UN[_MEASURE].values)
    ret = "U10 %s/%s/%s/%s :: r(%s)=%s,p=%s" %(_LEFTLABEL,_RIGHTLABEL,_METHOD,_MEASURE,dfN,pearson_coef,p_value)
    print(ret)


    ##### U8
    UNidx=ss.Age<=8
    UN=ss[UNidx]
    dfN=len(UN.index)
     
    pearson_coef, p_value = stats.pearsonr( UN['Age'].values,UN[_MEASURE].values)
    ret = "U8 %s/%s/%s/%s :: r(%s)=%s,p=%s" %(_LEFTLABEL,_RIGHTLABEL,_METHOD,_MEASURE,dfN,pearson_coef,p_value)
    print(ret)


    ##### U6
    UNidx=ss.Age<=6
    UN=ss[UNidx]
    dfN=len(UN.index)
     
    pearson_coef, p_value = stats.pearsonr( UN['Age'].values,UN[_MEASURE].values)
    ret = "U6 %s/%s/%s/%s :: r(%s)=%s,p=%s" %(_LEFTLABEL,_RIGHTLABEL,_METHOD,_MEASURE,dfN,pearson_coef,p_value)
    print(ret)


    ##### U5
    UNidx=ss.Age<=5
    UN=ss[UNidx]
    dfN=len(UN.index)
     
    pearson_coef, p_value = stats.pearsonr( UN['Age'].values,UN[_MEASURE].values)
    ret = "U5 %s/%s/%s/%s :: r(%s)=%s,p=%s" %(_LEFTLABEL,_RIGHTLABEL,_METHOD,_MEASURE,dfN,pearson_coef,p_value)
    print(ret)        


    ##### U4
    UNidx=ss.Age<=4
    UN=ss[UNidx]
    dfN=len(UN.index)
     
    pearson_coef, p_value = stats.pearsonr( UN['Age'].values,UN[_MEASURE].values)
    ret = "U4 %s/%s/%s/%s :: r(%s)=%s,p=%s" %(_LEFTLABEL,_RIGHTLABEL,_METHOD,_MEASURE,dfN,pearson_coef,p_value)
    print(ret)


    ##### U3
    UNidx=ss.Age<=3
    UN=ss[UNidx]
    dfN=len(UN.index)
     
    pearson_coef, p_value = stats.pearsonr( UN['Age'].values,UN[_MEASURE].values)
    ret = "U3 %s/%s/%s/%s :: r(%s)=%s,p=%s" %(_LEFTLABEL,_RIGHTLABEL,_METHOD,_MEASURE,dfN,pearson_coef,p_value)
    print(ret)    


    ##### U2
    UNidx=ss.Age<=2
    UN=ss[UNidx]
    dfN=len(UN.index)
     
    pearson_coef, p_value = stats.pearsonr( UN['Age'].values,UN[_MEASURE].values)
    ret = "U2 %s/%s/%s/%s :: r(%s)=%s,p=%s" %(_LEFTLABEL,_RIGHTLABEL,_METHOD,_MEASURE,dfN,pearson_coef,p_value)
    print(ret)    