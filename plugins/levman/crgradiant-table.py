#!/usr/bin/env python
import sys,os
import pandas as pd

diffusionpath=str(sys.argv[1])
print(f"[{diffusionpath}]")
bvec_fname=""
dwifiles=os.listdir(diffusionpath)
for f in dwifiles:
    if f.endswith('bvec'):
        bvec_fname=f"{diffusionpath}/{f}"
        break  #Get the first one I can find, we are only processing the first scan of this session
    if f=='bvecs':
        bvec_fname=f"{diffusionpath}/{f}"
        break
if bvec_fname=="":
    raise Exception(f'No bvec file found in [{diffusionpath}].  Cannot establish gradient table.')

csv = pd.read_csv(bvec_fname, skiprows=0,sep='\s+')
df_csv = pd.DataFrame(data=csv)
transposed_csv = df_csv.T        
transposed_csv.to_csv("bvecs2gradientMatrix.txt",header=False,index=True)

