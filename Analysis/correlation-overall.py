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

    _MEASURE=sys.argv[6]

    print("Parsing file %s" %(_DATAFILE))
    
    df = pd.read_csv(_DATAFILE)#.replace(np.nan, 0, regex=True) #nrows=30
    #df.to_pickle('/mnt/d/PROJECTS/2019-06-07.mid.csv.pk')
    #df = pd.read_pickle('/media/dmattie/GENERAL/2019-06-07.mid.csv.pk')

    all =df[['Age',_MEASURE]].copy()
    allna=all[all[_MEASURE].notna()]
    pearson_coef, p_value = stats.pearsonr( allna['Age'].values,allna[_MEASURE].values)
    print(pearson_coef,p_value)
    