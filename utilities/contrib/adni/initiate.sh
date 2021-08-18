#!/bin/bash

fshift() { local v n=$'\n';read -r v < <(
	    sed -e $'1{w/dev/stdout\n;d}' -i~ "$1")
	        printf ${2+-v} $2 "%s${n[${2+2}]}" "$v"
	}

fsplice() {
    [ "$2" ] || return ; local v n=$'\n';read -r v < <(
    sed -e $2$'{w/dev/stdout\n;d}' -i~ "$1");
    printf ${3+-v} $3 "%s${n[${3+3}]}" "$v"
}

PATIENT_QUEUE=~/projects/def-dmattie/data/adni-queue
ROOT_DIR=~/projects/rrg-jlevman/shared/adni
SUBJECTS_DIR=$ROOT_DIR/stage_0
util=$(pwd)


if [ $# -eq 0 ]
  then
      echo "No arguments supplied.  Getting next in queue $PATIENT_QUEUE"
      while [ ! -f $PATIENT_QUEUE ]
      do
        echo "."
	    sleep 2
      done
      mv $PATIENT_QUEUE $PATIENT_QUEUE.tmp

      fshift $PATIENT_QUEUE.tmp patientID  
      mv $PATIENT_QUEUE.tmp $PATIENT_QUEUE
          
else    
    myline=`awk "/$1/{ print NR; exit }" $PATIENT_QUEUE`
    if [ $myline ]
    then

        while [ ! -f $PATIENT_QUEUE ]
        do
            echo "."
            sleep 2
        done
        mv $PATIENT_QUEUE $PATIENT_QUEUE.tmp

        fsplice $PATIENT_QUEUE.tmp $myline patientID
        mv $PATIENT_QUEUE.tmp $PATIENT_QUEUE
        
        echo "Patient found on line $myline of $PATIENT_QUEUE"
    else    
        echo "Not found in QUEUE.  Queue file ignored"
        patientID=$1
    fi        
fi

echo "Initiating patient: $patientID"

echo "****START************"
if [ ! -d "$ROOT_DIR/stage_0/$patientID" ] &&
[ ! -d "$ROOT_DIR/stage_1/$patientID" ] &&
[ ! -d "$ROOT_DIR/stage_2/$patientID" ] &&
[ ! -d "$ROOT_DIR/stage_3/$patientID" ] &&
[ ! -d "$ROOT_DIR/stage_4/$patientID" ] ; then
  # Looks like we haven't seen this patient yet    
    cat $util/cascade_raw_to_0.sh.template | sed -e "s/PATIENT_RAW_0/$patientID/" > ~/jobs/generated/$patientID-raw_0.sh    
    chmod u+x ~/jobs/generated/$patientID-raw_0.sh
    cd ~/jobs/generated/logs    
    ##########################
    echo "*****RUN raw-0***********"
    ls -l ~/jobs/generated/$patientID-raw_0.sh     
   # sbatch ~/jobs/generated/$patientID-raw_0.sh 
    echo "*****END RUN raw-0********"
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
