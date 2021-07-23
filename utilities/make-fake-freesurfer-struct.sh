#!/bin/bash

if (($#==1));
then
    path=$1    
    for dir in $path/*/
    do
        dir=${dir%*/}       
        mkdir -p $dir/T1w/Freesurfer/mri
        touch $dir/T1w/Freesurfer/mri/wmparc.mgz
    done
    echo "Done"
else
    echo "Pass subject directory as arg"
fi