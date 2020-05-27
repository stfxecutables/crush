#!/bin/bash

echo "Working in $SUBJECTS_DIR | Sample: $1  Parcellating $2"
mri_extract_label $SUBJECTS_DIR/$1/T1w/$1/mri/wmparc.mgz $2 $SUBJECTS_DIR/$1/T1w/$1/mri/wmparc$2.mgz
mri_convert -rt nearest -nc -ns 1 $SUBJECTS_DIR/$1/T1w/$1/mri/wmparc$2.mgz $SUBJECTS_DIR/$1/T1w/$1/mri/wmparc$2.nii
