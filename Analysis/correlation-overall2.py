import pandas as pd
from scipy import stats   
import os,sys

if __name__=="__main__":
    
    _DATAFILE = sys.argv[1]

    ##Sample tiny datafile
    
    #ID,Age,m1,m2,m3
    #1,35,0.00234,0.1,1
    #2,30,0.0034,0.2,2
    #3,40,0.0013,0.3,4

    _MEASURE=sys.argv[2]

    print("Parsing file %s" %(_DATAFILE))
    
    df = pd.read_csv(_DATAFILE)
    print(f"Corellating {_MEASURE} with Age")
    all =df[['Age',_MEASURE]].copy()
    allna=all[all[_MEASURE].notna()]
    pearson_coef, p_value = stats.pearsonr( allna['Age'].values,allna[_MEASURE].values)
    print(pearson_coef,p_value)
    