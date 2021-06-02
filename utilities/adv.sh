#!/bin/bash
#SBATCH --time=0:1:00
#SBATCH --account=def-dmattie
#SBATCH --cpus-per-task=1
#SBATCH --mail-user=dmattie@stfx.ca
#SBATCH --error=%x-%j.err

echo $1 | touch "$1.log"

#patientID=$(sed -n "${SLURM_ARRAY_TASK_ID}"p ~/projects/def-dmattie/data/subjects.dat)
#patientID=101006

#SUBJECTS_DIR=~/scratch/HCP/stage_0
#pwd
#parcels=$(wc -l data/rois.txt)
#echo "$parcels rois"

#rendered=$(ls $SUBJECTS_DIR/$patientID/T1w/Tractography/parcellations|wc -l)
#echo "$rendered rendered"


