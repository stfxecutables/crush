import os, sys,inspect
import subprocess
import numpy as np
import re
import time
import uuid
from basecrush.pluginloader import pluginloader


from basecrush.ux import MsgUser
import nibabel as nib
from shutil import copyfile
from multiprocessing import Pool,cpu_count
import csv
import warnings
from collections import defaultdict
import json

              
class Visit:
   
    
                    
    def __init__(self,path,rebuild,voi,recrush,fixmissing,maxcores,disable_log):        
        self.VisitId=os.path.basename(path)
        self.path=path
        self.rebuild=rebuild
        self.voi=voi        
        self.recrush=recrush
        self.fixmissing=fixmissing        
        if maxcores:
            self.maxcores=maxcores 
        else:
            self.maxcores=9999
        self.data = defaultdict(list)#{}
        self.PatientId=os.path.split(os.path.dirname(self.path))[1]
        reconTest= "%s/Freesurfer/mri/wmparc.mgz" % (path)
        self.disable_log=disable_log
        
        if os.path.isfile(reconTest):
            self.ReconComplete=True            
        else:
            self.ReconComplete=False

        measurementTest = "%s/Tractography/crush/tracts.txt" % (path)
        #print(measurementTest)
        if os.path.isfile(measurementTest):
            self.MeasurementComplete=True    
        else: 
            self.MeasurementComplete=False


        self.Segments = []#{}

        i=1
        segmentMap="%s/%s" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),"segmentMap.txt")
        with open(segmentMap) as fin:
            reader=csv.reader(fin, skipinitialspace=True, quotechar="'")
            p = re.compile('^ *#')   # if not commented          
            for row in reader:
                #print("%s,%s" %(i,row))
                if(not p.match(row[0])): 
                    self.Segments.append({'roi':row[0],'roiname':row[1],'asymmetry':row[2]})
                i=i+1
        self.GetMeasurements()

    def Render(self):
        #Lets Render as needed
        MsgUser.message("Rendering %s" % self.path)
        
        for i in pluginloader.getPlugins():
            MsgUser.message("Invoking plugin " + i["name"])
            plugin = pluginloader.loadPlugin(i)
            plugin.run(self)

    def Measure(self):

        '''
        self.track_vis()
        '''
    def SetValue(self,name,value):
        self.data[self.PatientId][self.VisitId][name]=value

    def GetValue(self,name):
        return self.data[self.PatientId][self.VisitId][name]

    def Commit(self):
        with open("%s/Tractography/crush/tracts.txt" % (self.path), "w") as crush_file:
            for m in self.data[self.PatientId][self.VisitId]: 
                if m[-8:] !="-asymidx":
                    crush_file.write("%s=%s\n" % (m,self.data[self.PatientId][self.VisitId][m]))

    def GetMeasurements(self):

        Measurements={}
        #print(self.Segments)
        self.data[self.PatientId]={}
        self.data[self.PatientId][self.VisitId]={}        
        if os.path.isfile("%s/Tractography/crush/tracts.txt" %(self.path)):
            with open("%s/Tractography/crush/tracts.txt" %(self.path)) as fMeasure:
                for line in fMeasure:
                    if line.strip() != "":
                        nvp=line.split("=")  
                        self.data[self.PatientId][self.VisitId][nvp[0]]=nvp[1].strip()
                        if self.is_number(nvp[1].strip()) and nvp[1].strip()!="nan":
                            Measurements[nvp[0]]=nvp[1].strip()
                        else:
                            Measurements[nvp[0]]="" #convert nan to missing value
            
        ## Add derived measures here
        #print("Deriving Asymmetry Indexes")
        
        asymMeasuresToAdd = {}
        for m in self.data[self.PatientId][self.VisitId]:
            if len(m)>8 and m[-8] != "-asymidx":
                m0 = re.match("^(\w+)-(\w+)-(\w+)-(\w+)",m)
                
                if m0:
                    l_roi = m0.group(1)
                    l_roiE = m0.group(2)
                    l_method = m0.group(3)
                    l_measure = m0.group(4)

                    l_roiC=""
                    l_roiEC=""

                    #print("%s, %s" %(l_roi,l_roiE))
                    for s in self.Segments:                        
                        if s['roi']==l_roi:                            
                            l_roiC = s['asymmetry']
                        if s['roi']==l_roiE:
                            l_roiEC = s['asymmetry']

                    asymCounterpart = "%s-%s-%s-%s" %(l_roiC,l_roiEC,l_method,l_measure)                    
                    if asymCounterpart in self.data[self.PatientId][self.VisitId]:
                        if self.is_number(self.data[self.PatientId][self.VisitId][m]) and self.is_number(self.data[self.PatientId][self.VisitId][asymCounterpart]) and float(self.data[self.PatientId][self.VisitId][asymCounterpart]) != 0:
                            asymIdx=float(self.data[self.PatientId][self.VisitId][m]) / float(self.data[self.PatientId][self.VisitId][asymCounterpart])                            
                            asymMeasuresToAdd["%s-asymidx" %(m)] = asymIdx
        for newm in asymMeasuresToAdd:
            if self.is_number(str(asymMeasuresToAdd[newm])):
                Measurements[newm]=str(asymMeasuresToAdd[newm])
            
        ## End of derived measures
        
        return Measurements
    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    