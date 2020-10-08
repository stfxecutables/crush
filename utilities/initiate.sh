#!/bin/bash

if [ $# -eq 0 ]
  then
      echo "No arguments supplied.  Must specify a patient  E.g. initiate.sh 1001234"
      exit
fi
ROOT_DIR=~/scratch/HCP
SUBJECTS_DIR=$ROOT_DIR/stage_0
util=$(pwd)
patientID=$1
echo $patientID
echo "****START************"
if [ ! -d "$ROOT_DIR/stage_0/$patientID" ] &&
[ ! -d "$ROOT_DIR/stage_1/$patientID" ] &&
[ ! -d "$ROOT_DIR/stage_2/$patientID" ] &&
[ ! -d "$ROOT_DIR/stage_3/$patientID" ] &&
[ ! -d "$ROOT_DIR/stage_4/$patientID" ] ; then
  # Looks like we haven't seen this patient yet    
    cat cascade_aws_to_0.sh.template | sed -e "s/PATIENT_AWS_0/$patientID/" > ~/jobs/generated/$patientID-aws_0.sh    
    chmod u+x ~/jobs/generated/$patientID-aws_0.sh
    cd ~/jobs/generated/logs    
    ##########################
    echo "*****RUN aws-0***********"
    ls -l ~/jobs/generated/$patientID-aws_0.sh     
    sbatch ~/jobs/generated/$patientID-aws_0.sh 
    echo "*****END RUN aws-0********"
else
    if [ -d "$ROOT_DIR/stage_0/$patientID" ]; then
        echo "THIS SAMPLE ALREADY EXISTS IN THE PIPELINE, STAGE 0"
        echo "Recommended next step: ~/jobs/generated/$patientID-0_1.sh"
    fi

    if [ -d "$ROOT_DIR/stage_1/$patientID" ]; then
        echo "THIS SAMPLE ALREADY EXISTS IN THE PIPELINE, STAGE 1"
        echo "Recommended next step: ~/jobs/generated/$patientID-1_2.sh"
    fi

    if [ -d "$ROOT_DIR/stage_2/$patientID" ]; then
        echo "THIS SAMPLE ALREADY EXISTS IN THE PIPELINE, STAGE 2"
        echo "Recommended next step: ~/jobs/generated/$patientID-2_3.sh"
    fi

    if [ -d "$ROOT_DIR/stage_3/$patientID" ]; then
        echo "THIS SAMPLE ALREADY EXISTS IN THE PIPELINE, STAGE 3"
    fi
    
    if [ -d "$ROOT_DIR/stage_4/$patientID" ]; then
        echo "THIS SAMPLE ALREADY EXISTS IN THE PIPELINE, STAGE 4"
    fi
fi
cd $util
