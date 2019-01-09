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