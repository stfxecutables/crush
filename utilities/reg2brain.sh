#!/bin/bash

FILES=vol*.n*
dwi=$1
ref=$2
echo "Registering DWI [$1] to Reference [$2]"
refextension=$(echo $ref|rev|cut -f 1 -d '.'|rev)
echo $refextension
if [ "$refextension" == "mgz" ]
then
	niiref=${ref/mgz/nii}
	mri_convert -rt nearest -nc -ns 1 $ref $niiref
else 
	niiref=$ref
fi

fslsplit $1
for f in $FILES
do
   fbase=$(echo $f|cut -f 1 -d '.')
   echo "flirt -in $f -ref $niiref -omat $fbase.RegTransform4D -out reg2ref.$fbase.nii.gz"
   flirt -in $f -ref $niiref -omat $fbase.RegTransform4D -out reg2ref.$fbase.nii.gz
done
fslmerge -a reg2brain.data.nii.gz reg2ref.*
mkdir stage_registration
mv vol* stage_registration
mv reg2ref* stage_registration
