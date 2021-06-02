#!/bin/bash

if [ $# -eq 0 ]
  then
      echo "No arguments supplied.  Must specify a patient  E.g. get.sh 1001234"
      exit
fi
util=$(pwd)
patientID=$1
echo $patientID
cat advance_stage_aws.sh.template | sed -e "s/PATIENT/$patientID/" > ~/jobs/generated/adv_stg_aws_$patientID.sh
chmod u+x ~/jobs/generated/adv_stg_aws_$patientID.sh
cd ~/jobs/generated/logs
sbatch ~/jobs/generated/adv_stg_aws_$patientID.sh
cd $util
