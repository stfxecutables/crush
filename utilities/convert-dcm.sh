#!/bin/bash

start=$1
find $start -type d |while read d
do
   dcms=`find $d -name *.dcm -maxdepth 1 -print|wc -l`
   if [[ "$dcms" -gt "0" ]];then
   #remove any previous conversions
    [ -f $d/*.json ] && rm $d/*.json
    [ -f $d/*.nii ] && rm $d/*.nii
    [ -f $d/*.bvec ] && rm $d/*.bvec
    [ -f $d/*.bval ] && rm $d/*.bval
   #perform conversion
    ~/bin/MRIcroGL/Resources/dcm2niix $d
   fi
done
