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

_OUTPUTPATH="."


if __name__=="__main__":
    
    _DATAFILE = sys.argv[1]
    _OUTPUTPATH=sys.argv[2]
    _INTERESTINGCSV=sys.argv[3]
    _MEASURE=sys.argv[4]
    
    print("Parsing file %s,rendering to %s" %(_DATAFILE,_OUTPUTPATH))    
    df = pd.read_csv(_DATAFILE)#.replace(np.nan, 0, regex=True) #nrows=30
    print("Looking for intersections")
    InterestingROI = pd.read_csv(_INTERESTINGCSV)


    


    plt.figure()
    genders = ['Male','Female']
    
    if not os.path.isdir(_OUTPUTPATH):
        os.mkdir(_OUTPUTPATH)

    fig,axs = plt.subplots(nrows=4,ncols=4,figsize=(25,25))
    for index, intersection in InterestingROI.iterrows():#IntersectionsDF.iterrows():
        #print(index+1)
        #print(intersection.keys)
        #print(intersection[0])
        
        #plt.subplot(4,4,index+1)
        roi=str(intersection[0])#.zfill(4)
        roiEnd=str(intersection[1])#.zfill(4)
        method=str(intersection[2])
        r=int(index/4)
        c=index%4
        print("r=%s,c=%s start:%s end%s method:%s" %(r,c,roi,roiEnd,method))
        
        plt.title="%s to %s (%s)" %(roi,roiEnd,method)

        subset1 =df[ (df['ROI Label']==roi) & (df['ROI END Label']==roiEnd) & (df['Method']==method)]

        allvals = subset1[_MEASURE].notna()
        nonzero_measures =subset1[allvals].copy()  

        nonzero_measures_x = nonzero_measures[[
            'Age', 
            'Gender',      
            _MEASURE
        ]]  
        males = nonzero_measures_x[nonzero_measures_x['Gender'] == "Male"]
        females = nonzero_measures_x[nonzero_measures_x['Gender'] == "Female"]

        #plt.plot(nonzero_measures_x.notna())
        m_slope, m_intercept, m_r_value, m_p_value, m_std_err = stats.linregress(males['Age'],males[_MEASURE])
        f_slope, f_intercept, f_r_value, f_p_value, f_std_err = stats.linregress(females['Age'],females[_MEASURE])    

        #gM = sns.regplot(x='Age',y=_MEASURE,data=males,ax=axs[r,c],scatter_kws={"color": "blue"}, line_kws={"color": "blue",'label': "y={0:.1f}x+{1:.1f} (r={1:.1f}, p={1:.1f}, std err={1:.1f})".format(m_slope,m_intercept,m_r_value, m_p_value, m_std_err)})
        #gF = sns.regplot(x='Age',y=_MEASURE,data=females,ax=axs[r,c],scatter_kws={"color": "red"}, line_kws={"color": "red",'label': "y={0:.1f}x+{1:.1f} (r={1:.1f}, p={1:.1f}, std err={1:.1f})".format(f_slope,f_intercept,f_r_value, f_p_value, f_std_err)})
        gM = sns.regplot(x='Age',y=_MEASURE,data=males,ax=axs[r,c],scatter_kws={"color": "blue"}, line_kws={"color": "blue",'label': "Males: y={0:.3f}x+{1:.3f}".format(m_slope,m_intercept)})
        gF = sns.regplot(x='Age',y=_MEASURE,data=females,ax=axs[r,c],scatter_kws={"color": "red"}, line_kws={"color": "red",'label': "Females: y={0:.3f}x+{1:.3f}".format(f_slope,f_intercept)})
        gM.legend()
        gF.legend()
        gM.set_title("%s / %s (%s)" %(roi,roiEnd,method))
        #sns.pairplot(nonzero_measures_x,hue="Gender",diag_kind='auto',kind='reg')            
    fig.tight_layout()    
    plt.savefig("%s/%s-Pairplot-all.png" %(_OUTPUTPATH,_MEASURE))
    plt.close() 
