#!/bin/bash

for d in ~/scratch/HCP/stage_0/*/ ; do
    patientID=$(basename "$d")
    echo $patientID
    cat advance_stage_0_to_1_parcellated.sh.template | sed -e "s/PATIENT/$patientID/" > ~/jobs/generated/advance_stage_0_$patientID.sh
    chmod u+x ~/jobs/generated/advance_stage_0_$patientID.sh
    mkdir -p ~/jobs/generated/logs
    cd ~/jobs/generated/logs
    sbatch ~/jobs/generated/advance_stage_0_$patientID.sh
done
