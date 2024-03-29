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


#_DATAFILE='/media/dmattie/GENERAL/2019-06-07.small.csv'
#_DATAFILE='/media/dmattie/crush/2019-06-07.mid.csv'
#_DATAFILE='/media/dmattie/GENERAL/full.csv'
_DATAFILE=sys.argv[1]#'~/projects/full.csv'
_OUTPUTPATH = sys.argv[2]

df = pd.read_csv(_DATAFILE)#.replace(np.nan, 0, regex=True) #nrows=30


##############################################################################
#
#        NUMTRACTS
#
##############################################################################

print("##########################\n#\n#  NumTracts\n#\n##########################")
ROIs=[
      ['ctx-lh-parahippocampa','ctx-lh-rostralanteriorcingulate','roi_end'],
      ['ctx-rh-pericalcarine','wm-lh-temporalpole','roi_end'],
      ['Left-Cerebellum-White-Matter','CC_Posterior','roi_end'],
      ['Right-vessel','ctx-rh-entorhinal','roi_end'],
      ['ctx-lh-superiorfrontal','wm-rh-middletemporal','roi_end'],      
      ]
#ROIs=[
#     ['ctx-rh-posteriorcingulate','ctx-rh-frontalpole','roi_end'],
#     ['Left-Cerebellum-White-Matter','ctx-lh-supramarginal','roi_end']
# ]
ROIs=[
    ['ctx-lh-inferiorparietal','wm-rh-caudalmiddlefrontal','roi'],
    ['Left-vessel','ctx-rh-parsorbitalis','roi'],
    ['Left-Caudate','Right-vessel','roi'],
    ['Left-vessel','wm-rh-parsorbitalis','roi'],
    ['Right-Hippocampus','ctx-rh-parsopercularis','roi'],
    ['ctx-rh-parsopercularis','wm-lh-lateraloccipital','roi'],
    ['4th-Ventricle','ctx-lh-caudalmiddlefrontal','roi'],
    ['Left-vessel','ctx-lh-parstriangularis','roi_end'],
    ['Left-Pallidum','ctx-lh-caudalmiddlefrontal','roi_end'],
    ['Left-VentralDC','ctx-rh-parsopercularis','roi_end'],
    ['Right-Pallidum','ctx-lh-parsorbitalis','roi']
]
      #2023-2032-roi_end-meanFA,0.9999999999999998,1.0,0.0


for focus in ROIs:
    print("ROI Start: "+focus[0]+", ROI End: "+focus[1]+", Method: "+focus[2])

    subset1 = df[ (df['ROI Label']==focus[0]) & 
                 (df['ROI END Label']==focus[1]) & 
                 (df['Method']==focus[2])]
    
    if subset1.shape[0]>0:
    
        allvals = subset1['NumTracts']>0   #################################      TODO
        nonzero_measures = subset1[allvals]
        
        nonzero_measures_only = nonzero_measures[[
            'Age',
            'NumTracts',
            'TractsToRender',
            'LinesToRender',
            'MeanTractLen',
            'MeanTractLen_StdDev',
            'VoxelSizeX',
            'VoxelSizeY',
            'VoxelSizeZ',
            'meanFA',
            'stddevFA',
            'meanADC',
            'stddevADC'
            ]]
        
        nonzero_measures_meanFA = nonzero_measures[[
            'Age',          
            'meanFA'
            ]]
        
        plt.figure()
        
        sns.regplot('Age','NumTracts',nonzero_measures)
        
        fa=("%s/visuals/%s-NumTracts.png" %(_OUTPUTPATH,focus))
        
        plt.title('Changes in log age vs log NumTracts')
        plt.xlabel('Age')                           ####################   TODO
        plt.ylabel('NumTracts')
        
        plt.savefig(fa)
        
        plt.figure()
        
        fb=("%s/visuals/%s-meanFA.png" %(_OUTPUTPATH,focus))
        sns.regplot('Age','meanFA',nonzero_measures)
        plt.title('Changes in log age vs log meanFA')
        plt.xlabel('Age')                           ####################   TODO
        plt.ylabel('meanFA')
                    
        plt.savefig(fb)

        plt.figure()
        
        fb=("%s/visuals/%s-meanADC.png" %(_OUTPUTPATH,focus))
        sns.regplot('Age','meanADC',nonzero_measures)
        plt.title('Changes in log age vs log meanADC')
        plt.xlabel('Age')                           ####################   TODO
        plt.ylabel('meanADC')
                    
        plt.savefig(fb)
        # Plot formatting
        
  
        plt.figure()
        
        sns.pairplot(nonzero_measures_meanFA,diag_kind='auto',plot_kws={'alpha':0.2})
        
        fc=("%s/visuals/%s-pairplot.png" %(_OUTPUTPATH,focus))
        plt.savefig(fc)
#    
#    #### HISTOGRAM
#    plt.figure()
#    plt.hist(nonzero_measures_male.meanFA, bins='auto', alpha=0.5, label='Male')
#    plt.hist(nonzero_measures_female.meanFA, bins='auto', alpha=0.5, label='Female')
#    plt.legend(loc='upper right')
#    plt.title('Histogram of NumTracts')                  ##################   TODO
#    plt.xlabel('NumTracts')                          #####################   TODO
#    plt.ylabel('Count')
#    plt.show()
#    
#
###############################################################################
##
##        TractsToRender
##
###############################################################################
#
#print("##########################\n#\n#  TractsToRender\n#\n##########################")
#ROIs=[
#      ['ctx-lh-parahippocampa','ctx-lh-rostralanteriorcingulate','roi_end'],
#      ['ctx-rh-pericalcarine','wm-lh-temporalpole','roi_end'],
#      ['Left-Cerebellum-White-Matter','CC_Posterior','roi_end'],
#      ['Right-vessel','ctx-rh-entorhinal','roi_end'],
#      ['ctx-lh-superiorfrontal','wm-rh-middletemporal','roi_end'],      
#      ]
#
#for focus in ROIs:
#    print("ROI Start: "+focus[0]+", ROI End: "+focus[1]+", Method: "+focus[2])
#
#    subset1 = df[ (df['ROI Label']==focus[0]) & 
#                 (df['ROI END Label']==focus[1]) & 
#                 (df['Method']==focus[2])]
#
#    allvals = subset1['TractsToRender']>0   #################################      TODO
#    nonzero_measures = subset1[allvals]
#    
#    males=nonzero_measures['Gender']=='Male'
#    females=nonzero_measures['Gender']=='Female'
#    
#    nonzero_measures_male = nonzero_measures[males]
#    nonzero_measures_female = nonzero_measures[females]
#   
#    ## SOURCE: https://towardsdatascience.com/histograms-and-density-plots-in-python-f6bda88f5ac0
#    
#    plt.figure()
#    genders = ['Male','Female']
#    
#    for gender in genders:
#        subset = nonzero_measures[nonzero_measures['Gender'] == gender]
#    
#        sns.distplot(subset['TractsToRender'], hist = False, kde = True, ######    TODO
#                     kde_kws = {'linewidth': 3},
#                     label = gender)
#        
#    # Plot formatting
#    plt.legend(prop={'size': 10}, title = 'Gender')
#    plt.title('Density Plot per Gender')
#    plt.xlabel('TractsToRender')                           ####################   TODO
#    plt.ylabel('Density')
#    
#    
#    #### HISTOGRAM
#    plt.figure()
#    plt.hist(nonzero_measures_male.meanFA, bins='auto', alpha=0.5, label='Male')
#    plt.hist(nonzero_measures_female.meanFA, bins='auto', alpha=0.5, label='Female')
#    plt.legend(loc='upper right')
#    plt.title('Histogram of TractsToRender')                  ##################   TODO
#    plt.xlabel('TractsToRender')                          #####################   TODO
#    plt.ylabel('Count')
#    plt.show()
#        
###############################################################################
##
##        MEAN FA
##
###############################################################################
#
#print("##########################\n#\n#  MEAN FA\n#\n##########################")
#ROIs=[
#      ['ctx-lh-parahippocampa','ctx-lh-rostralanteriorcingulate','roi_end'],
#      ['ctx-rh-pericalcarine','wm-lh-temporalpole','roi_end'],
#      ['Left-Cerebellum-White-Matter','CC_Posterior','roi_end'],
#      ['Right-vessel','ctx-rh-entorhinal','roi_end'],
#      ['ctx-lh-superiorfrontal','wm-rh-middletemporal','roi_end'],      
#      ]
#
#for focus in ROIs:
#    print("ROI Start: "+focus[0]+", ROI End: "+focus[1]+", Method: "+focus[2])
#
#    subset1 = df[ (df['ROI Label']==focus[0]) & 
#                 (df['ROI END Label']==focus[1]) & 
#                 (df['Method']==focus[2])]
#
#    allvals = subset1['meanFA']>0   #################################      TODO
#    nonzero_measures = subset1[allvals]
#    
#    males=nonzero_measures['Gender']=='Male'
#    females=nonzero_measures['Gender']=='Female'
#    
#    nonzero_measures_male = nonzero_measures[males]
#    nonzero_measures_female = nonzero_measures[females]
#   
#    ## SOURCE: https://towardsdatascience.com/histograms-and-density-plots-in-python-f6bda88f5ac0
#    
#    plt.figure()
#    genders = ['Male','Female']
#    
#    for gender in genders:
#        subset = nonzero_measures[nonzero_measures['Gender'] == gender]
#    
#        sns.distplot(subset['meanFA'], hist = False, kde = True, ######    TODO
#                     kde_kws = {'linewidth': 3},
#                     label = gender)
#        
#    # Plot formatting
#    plt.legend(prop={'size': 10}, title = 'Gender')
#    plt.title('Density Plot per Gender')
#    plt.xlabel('mean FA')                           ####################   TODO
#    plt.ylabel('Density')
#    
#    
#    #### HISTOGRAM
#    plt.figure()
#    plt.hist(nonzero_measures_male.meanFA, bins='auto', alpha=0.5, label='Male')
#    plt.hist(nonzero_measures_female.meanFA, bins='auto', alpha=0.5, label='Female')
#    plt.legend(loc='upper right')
#    plt.title('Histogram of meanFA')                  ##################   TODO
#    plt.xlabel('mean FA')                          #####################   TODO
#    plt.ylabel('Count')
#    plt.show()
#
#
###############################################################################
##
##        stddevFA
##
###############################################################################
#
#print("##########################\n#\n#  stddevFA\n#\n##########################")
#ROIs=[
#      ['ctx-lh-parahippocampa','ctx-lh-rostralanteriorcingulate','roi_end'],
#      ['ctx-rh-pericalcarine','wm-lh-temporalpole','roi_end'],
#      ['Left-Cerebellum-White-Matter','CC_Posterior','roi_end'],
#      ['Right-vessel','ctx-rh-entorhinal','roi_end'],
#      ['ctx-lh-superiorfrontal','wm-rh-middletemporal','roi_end'],      
#      ]
#
#for focus in ROIs:
#    print("ROI Start: "+focus[0]+", ROI End: "+focus[1]+", Method: "+focus[2])
#
#    subset1 = df[ (df['ROI Label']==focus[0]) & 
#                 (df['ROI END Label']==focus[1]) & 
#                 (df['Method']==focus[2])]
#
#    allvals = subset1['stddevFA']>0   #################################      TODO
#    nonzero_measures = subset1[allvals]
#    
#    males=nonzero_measures['Gender']=='Male'
#    females=nonzero_measures['Gender']=='Female'
#    
#    nonzero_measures_male = nonzero_measures[males]
#    nonzero_measures_female = nonzero_measures[females]
#   
#    ## SOURCE: https://towardsdatascience.com/histograms-and-density-plots-in-python-f6bda88f5ac0
#    
#    plt.figure()
#    genders = ['Male','Female']
#    
#    for gender in genders:
#        subset = nonzero_measures[nonzero_measures['Gender'] == gender]
#    
#        sns.distplot(subset['stddevFA'], hist = False, kde = True, ######    TODO
#                     kde_kws = {'linewidth': 3},
#                     label = gender)
#        
#    # Plot formatting
#    plt.legend(prop={'size': 10}, title = 'Gender')
#    plt.title('Density Plot per Gender')
#    plt.xlabel('stddevFA')                           ####################   TODO
#    plt.ylabel('Density')
#    
#    
#    #### HISTOGRAM
#    plt.figure()
#    plt.hist(nonzero_measures_male.meanFA, bins='auto', alpha=0.5, label='Male')
#    plt.hist(nonzero_measures_female.meanFA, bins='auto', alpha=0.5, label='Female')
#    plt.legend(loc='upper right')
#    plt.title('Histogram of stddevFA')                  ##################   TODO
#    plt.xlabel('stddevFA')                          #####################   TODO
#    plt.ylabel('Count')
#    plt.show()
#            
#
###############################################################################
##
##        MEAN ADC
##
###############################################################################
#
#print("##########################\n#\n#  MEAN ADC\n#\n##########################")
#ROIs=[
#      ['Right-Putamen','wm-lh-parsorbitalis','roi_end'],
#      ['ctx-lh-parahippocampal','ctx-lh-rostralanteriorcingulate','roi_end'],
#      ['Left-Pallidum','ctx-rh-postcentral','roi_end'],
#      ['Left-Amygdala','Right-Inf-Lat-Vent','roi_end'],
#      ['CC_Anterior','ctx-lh-lateraloccipital','roi_end'],      
#      ]
#
#for focus in ROIs:
#    print("ROI Start: "+focus[0]+", ROI End: "+focus[1]+", Method: "+focus[2])
#
#    subset1 = df[ (df['ROI Label']==focus[0]) & 
#                 (df['ROI END Label']==focus[1]) & 
#                 (df['Method']==focus[2])]
#
#    allvals = subset1['meanADC']>0   #################################      TODO
#    nonzero_measures = subset1[allvals]
#    
#    males=nonzero_measures['Gender']=='Male'
#    females=nonzero_measures['Gender']=='Female'
#    
#    nonzero_measures_male = nonzero_measures[males]
#    nonzero_measures_female = nonzero_measures[females]
#   
#    ## SOURCE: https://towardsdatascience.com/histograms-and-density-plots-in-python-f6bda88f5ac0
#    
#    plt.figure()
#    genders = ['Male','Female']
#    
#    for gender in genders:
#        subset = nonzero_measures[nonzero_measures['Gender'] == gender]
#    
#        sns.distplot(subset['meanADC'], hist = False, kde = True, ######    TODO
#                     kde_kws = {'linewidth': 3},
#                     label = gender)
#        
#    # Plot formatting
#    plt.legend(prop={'size': 10}, title = 'Gender')
#    plt.title('Density Plot per Gender')
#    plt.xlabel('mean ADC')                           ####################   TODO
#    plt.ylabel('Density')
#    
#    
#    #### HISTOGRAM
#    plt.figure()
#    plt.hist(nonzero_measures_male.meanFA, bins='auto', alpha=0.5, label='Male')
#    plt.hist(nonzero_measures_female.meanFA, bins='auto', alpha=0.5, label='Female')
#    plt.legend(loc='upper right')
#    plt.title('Histogram of meanADC')                  ##################   TODO
#    plt.xlabel('mean ADC')                          #####################   TODO
#    plt.ylabel('Count')
#    plt.show()
#    
#
#
###############################################################################
##
##        stddevADC
##
###############################################################################
#
#print("##########################\n#\n#  stddevADC\n#\n##########################")
#ROIs=[
#      ['Right-Putamen','wm-lh-parsorbitalis','roi_end'],
#      ['ctx-lh-parahippocampal','ctx-lh-rostralanteriorcingulate','roi_end'],
#      ['Left-Pallidum','ctx-rh-postcentral','roi_end'],
#      ['Left-Amygdala','Right-Inf-Lat-Vent','roi_end'],
#      ['CC_Anterior','ctx-lh-lateraloccipital','roi_end'],      
#      ]
#
#for focus in ROIs:
#    print("ROI Start: "+focus[0]+", ROI End: "+focus[1]+", Method: "+focus[2])
#
#    subset1 = df[ (df['ROI Label']==focus[0]) & 
#                 (df['ROI END Label']==focus[1]) & 
#                 (df['Method']==focus[2])]
#
#    allvals = subset1['stddevADC']>0   #################################      TODO
#    nonzero_measures = subset1[allvals]
#    
#    males=nonzero_measures['Gender']=='Male'
#    females=nonzero_measures['Gender']=='Female'
#    
#    nonzero_measures_male = nonzero_measures[males]
#    nonzero_measures_female = nonzero_measures[females]
#   
#    ## SOURCE: https://towardsdatascience.com/histograms-and-density-plots-in-python-f6bda88f5ac0
#    
#    plt.figure()
#    genders = ['Male','Female']
#    
#    for gender in genders:
#        subset = nonzero_measures[nonzero_measures['Gender'] == gender]
#    
#        sns.distplot(subset['stddevADC'], hist = False, kde = True, ######    TODO
#                     kde_kws = {'linewidth': 3},
#                     label = gender)
#        
#    # Plot formatting
#    plt.legend(prop={'size': 10}, title = 'Gender')
#    plt.title('Density Plot per Gender')
#    plt.xlabel('stddevADC')                           ####################   TODO
#    plt.ylabel('Density')
#    
#    
#    #### HISTOGRAM
#    plt.figure()
#    plt.hist(nonzero_measures_male.meanFA, bins='auto', alpha=0.5, label='Male')
#    plt.hist(nonzero_measures_female.meanFA, bins='auto', alpha=0.5, label='Female')
#    plt.legend(loc='upper right')
#    plt.title('Histogram of stddevADC')                  ##################   TODO
#    plt.xlabel('stddevADC')                          #####################   TODO
#    plt.ylabel('Count')
#    plt.show()
#    
#
#
