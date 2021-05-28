import os, sys, argparse,re
import csv

import pandas as pd

import numpy as np
import pandas as pd

# _mat = pd.read_csv("bvecs")
# _mat = _mat[_mat.columns[0:3]].values
# _t_mat = np.transpose(_mat)

# print(_t_mat)

#a = izip(*csv.reader(open('bvecs', "rt")))
#csv.writer(open('gtab', "wt")).writerows(a)


pd.read_csv('bvecs', header=None).T.to_csv('gtab', header=False, index=False)

csv = pd.read_csv("bvecs" , skiprows=0,sep=' ')
df_csv = pd.DataFrame(data=csv)
transposed_csv = df_csv.T
print(transposed_csv)
transposed_csv.to_csv('bvecs2gradientMatrix.txt',header=False,index=True)
#np.savetxt("bvecs2gradientMatrix.txt", transposed_csv,delimiter=",", fmt='%1.6f')

