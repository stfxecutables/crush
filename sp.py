import subprocess

with open("abc.txt", "w") as lsout:
#	proc=subprocess.run(["ls"],stdout=lsout,text=True)
	proc=subprocess.run(["ls"],capture_output=True,text=True)
	print(proc.stdout)
