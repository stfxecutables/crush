import os

dwifiles=os.listdir('/media/dmattie/GENERAL/schizconnect/data/sub-A00000300/ses-20110101/dwi/')
for f in dwifiles:
    if f.endswith('bvec'):
        print(f)
        break