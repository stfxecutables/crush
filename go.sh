#!/bin/bash
#SBATCH --time=11:30:00
#SBATCH --account=def-jlevman
#SBATCH --array=3-4
#SBATCH --mem-per-cpu=2000M
#SBATCH --cpus-per-task=32
#SBATCH --mail-user=dmattie@stfx.ca
#SBATCH --mail-type=ALL
printf -v patientID "%04d" $SLURM_ARRAY_TASK_ID
patientID="0003"
echo $patientID
#rsync -a ~/projects/def-jlevman/dmattie/crushdata/$patientID/ ~/scratch/crushdata/$patientID/
exitstatus=$?
exitstatus=0
if [ $exitstatus -eq 0 ];then
	echo "Successfully staged $patientID"
	python3 ~/projects/def-jlevman/dmattie/crush/crush -samples ~/scratch/crushdata -patient $patientID -fixmissing
	rsync -a ~/scratch/crushdata/$patientID ~/projects/def-jlevman/dmattie/crushdata/$patientID/ 
        exitstatus=$?
	if  [ $exitstatus -eq 0 ];then
		echo "Returned changes back to project directory"
		rsync -a --delete ~/scratch/crushdata/null/ ~/scratch/crushdata/$patientID/
	else
		echo "FAILED to return changes to project directory"
	fi
else
	echo "Failed to stage $patientID"
fi

