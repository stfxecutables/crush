#!/bin/bash

if [ $# -eq 0 ]
  then
      echo "No arguments supplied.  Must specify a stage number.  E.g. advance.sh 0"
      exit
fi

util=$(pwd)
for d in ~/scratch/HCP/stage_$1/*/ ; do
    patientID=$(basename "$d")
    echo $patientID
    cat advance_stage_$1.sh.template | sed -e "s/PATIENT/$patientID/" > ~/jobs/generated/advance_stage_$1_$patientID.sh
    chmod u+x ~/jobs/generated/advance_stage_$1_$patientID.sh
    mkdir -p ~/jobs/generated/logs
    cd ~/jobs/generated/logs
    sbatch ~/jobs/generated/advance_stage_$1_$patientID.sh
    cd $util
done
