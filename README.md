# README #


### What is this repository for? ###

It basically does this at the moment:
* Iterate the patient samples and each patient visit.
* Where it looks like something is incomplete, complete that part of the workflow above, otherwise skip – I know my tests for readiness are incomplete here
* Take some measurements once completed

### How do I get set up? ###

Running Tests:

Create a folder Patients and fill with samples 0001, 0002

`python atlas.py ~/Documents/Patients`

#Virtual Environment
`python3 -m venv ~/projects/environmens/crush`
`source ~/projects/environments/crush/bin/activate`

#Executions
./crush -samples /media/dmattie/GENERAL/CRUSHDATA -status
./crush -samples /media/dmattie/GENERAL/CRUSHDATA 

#Issues with old python 3 libss
try:
sudo pip3 install -U nibabel


#libgsl.so.0

whereis libgsl.so.0
GSL is provided by the "gsl" module. However in your case you have a precompiled application. You'd either need to compile it from source or try this which would be easier:

module load gsl/1.16
setrpaths.sh --path ~/projects/def-jlevman/dmattie/bin/dtk --add_path=$EBROOTGSL/lib

this modifies the binaries in that folder to look in $EBROOTGSL/lib which contains libgsl.so.0.

#GLobus
    ./globusconnect -start

    55167189


find . -name *.json -print > ~/allgjson.txt

tar -cvf allgjson.tar -T ~/allgjson.txt


find . -name *.out -print | tar -zcvf outs.tar.gz -T 

find /scratch/dmattie/crushdata -name *.json -print  | xargs tar -czvf ~/projects/dmattie/json.tar.gz 


