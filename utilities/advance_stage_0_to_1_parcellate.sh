#!/bin/bash
#SBATCH --time=0:40:00
#SBATCH --account=def-dmattie
#SBATCH --array=4-101
#SBATCH --cpus-per-task=1
#SBATCH --mail-user=dmattie@stfx.ca
#SBATCH --mem-per-cpu=1000M
#SBATCH --error=%x-%j.err

patientID=$(sed -n "${SLURM_ARRAY_TASK_ID}"p ~/projects/def-dmattie/data/subjects.dat)
#patientID=100408
#patientID=100610

SUBJECTS_DIR=~/scratch/HCP/stage_0
JOBSDIR=$(pwd)

while read p; do
    echo "Extracting Region $p ($SUBJECTS_DIR/$patientID/T1w/Tractography/parcellations)"
    mkdir -p $SUBJECTS_DIR/$patientID/T1w/Tractography/parcellations
    cp $SUBJECTS_DIR/$patientID/T1w/$patientID/mri/wmparc.mgz $SUBJECTS_DIR/$patientID/T1w/Tractography/parcellations
    cd $SUBJECTS_DIR/$patientID/T1w/Tractography/parcellations

    mri_convert -rt nearest -nc -ns 1 wmparc.mgz wmparc.nii
    mri_extract_label wmparc.nii $p wmparc$p.nii


done <$JOBSDIR/data/rois.txt

parcels=$(cat $JOBSDIR/data/rois.txt|wc -l)
echo "$parcels rois"

rendered=$(ls $SUBJECTS_DIR/$patientID/T1w/Tractography/parcellations|wc -l) 
echo "$rendered rendered"

if [ "$rendered" -ge "$parcels" ]; then
    mkdir -p $SUBJECTS_DIR/../stage_1 
    mv $SUBJECTS_DIR/$patientID $SUBJECTS_DIR/../stage_1

fi

