#!/bin/bash

start=$1
find $start -type d |while read d
do
   dcms=`find $d -name *.dcm -maxdepth 1 -print|wc -l`
   if [[ "$dcms" -gt "0" ]];then
   #remove any previous conversions
    rm $d/*.json
    rm $d/*.nii
    rm $d/*.bvec
    rm $d/*.bval
    ~/bin/MRIcroGL/Resources/dcm2niix $d
   fi
done
