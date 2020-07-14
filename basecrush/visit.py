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
   
    
                    
    def __init__(self,path,rebuild,voi,recrush,fixmissing,maxcores,disable_log,pipeline):        
        self.SourceTaxonomy="undefined"
        self.VisitId=os.path.basename(path)
        self.path=path
        self.freesurferpath="undefined"
        self.tractographypath="undefined"
        self.diffusionpath="undefined"
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
            print("Looks like BCH formatted directory structure")
            self.SourceTaxonomy="BCH"
            self.ReconComplete=True   
            self.freesurferpath = "%s/Freesurfer" % (path)   
            self.tractographypath = "%s/Tractography" % (path) 
            self.diffusionpath = "%s/Tractography" %(path)    
        else:
            
            if os.path.isfile("%s/%s/mri/wmparc.mgz" % (path,self.PatientId)):
                self.SourceTaxonomy="HCP"
                print("Looks like HCP formatted directory structure")
                self.ReconComplete=True
                self.freesurferpath = "%s/%s" % (path,self.PatientId)

             
                self.tractographypath = "%s/Tractography" % (path)
                self.diffusionpath = "%s/Diffusion" %(path) 
            else:
                self.ReconComplete=False
        self.pipeline=pipeline

        measurementTest = "%s/crush/tracts.txt" % (self.tractographypath)
        
        if os.path.isfile(measurementTest):
            self.MeasurementComplete=True    
        else: 
            self.MeasurementComplete=False
        
        self.GetMeasurements()

    def Render(self):
        #Lets Render as needed
        MsgUser.message("Rendering %s" % self.path)
        
        for i in pluginloader.getPlugins():
                      
            if(self.pipeline==None or i["name"]==self.pipeline):
                MsgUser.message("Invoking plugin " + i["name"])
                plugin = pluginloader.loadPlugin(i)                
                plugin.run(self)

    def SetValue(self,pipelineId,name,value):            
        self.data[self.PatientId][self.VisitId]["%s/%s" %(pipelineId,name)]=value        

    def GetValue(self,pipelineId,name):
        return self.data[self.PatientId][self.VisitId]["%s/%s" %(pipelineId,name)]

    def Commit(self):
        with open("%s/crush/tracts.txt" % (self.tractographypath), "w") as crush_file:
            for m in self.data[self.PatientId][self.VisitId]: 
                if m[-8:] !="-asymidx":
                    crush_file.write("%s=%s\n" % (m,self.data[self.PatientId][self.VisitId][m]))

    def GetMeasurements(self):

        Measurements={}
        #print(self.Segments)
        self.data[self.PatientId]={}
        self.data[self.PatientId][self.VisitId]={}        
        if os.path.isfile("%s/crush/tracts.txt" %(self.tractographypath)):
            with open("%s/crush/tracts.txt" %(self.tractographypath)) as fMeasure:
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
        
        
        
        return Measurements
    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def Report2(self):
        #MsgUser.bold("Reporting values of interest")

        if os.path.isfile("%s" %(self.voi)):
            #Determine my interests
            with open(self.voi) as f:
                voi_interests = f.readlines()
                voi_interests = [x.strip() for x in voi_interests] #Remove Whitespace
            #Get everything
            self.data[self.PatientId]={}
            self.data[self.PatientId][self.VisitId]={}

            if os.path.isfile("%s/crush/tracts.txt" %(self.tractographypath)):
                with open("%s/crush/tracts.txt" %(self.tractographypath)) as fMeasure:
                    for line in fMeasure:
                        nvp=line.split("=")   
                        self.data[self.PatientId][self.VisitId][nvp[0]]=nvp[1].strip()
            
            ## Add derived measures here
            #print("Deriving Asymmetry Indexes")
            for s in self.Segments:  
                roi=s['roi']                             
                asymmetry=s['asymmetry']
                if asymmetry:
                    for p in self.data:
                        for v in self.data[p]: 
                            asymMeasuresToAdd = {}
                            for m in self.data[p][v]:
                                #For all measures                                                                                      
                                searchEx="%s-%s" %(roi,r'(\d+)')
                                roiGrp = re.search(searchEx, m)
                                if roiGrp:
                                    ma=m.replace(roi,asymmetry)
                                    if ma in self.data[p][v] and float(self.data[p][v][ma]) != 0:
                                        asymIdx=float(self.data[p][v][m]) / float(self.data[p][v][ma])
                                    else:
                                        asymIdx=0
                                    #self.data[self.PatientId][self.VisitId][ma]=asymIdx
                                    
                                    asymMeasuresToAdd["%s-asymidx" %(ma)]=asymIdx
                                    #print("%s [%s] has aymmetry with %s [%s].  ASYM IDX=[%s]" %(m,self.data[p][v][m],ma,self.data[p][v][ma],asymIdx))
                                    #print("%s is %s" %(ma,asymIdx))
                            for ma in asymMeasuresToAdd:                                                                
                                #print("XX-%s" %(ma))
                                self.data[p][v][ma] = str(asymMeasuresToAdd[ma])

                    
            ## End of derived measures

            #Print report
            for p in self.data:
                for v in self.data[p]:
                    row=[]
                    row.append(p)
                    row.append(v)
                    for m in voi_interests:
                        if m in self.data[p][v]:
                            row.append(self.data[p][v][m])
                            if "%s-asymidx" %(m) in self.data[p][v]:
                                row.append(self.data[p][v]["%s-asymidx" %(m)])
                        else:
                            row.append("")
            print(",".join(row))                                               

    def Report(self):
        #MsgUser.bold("Reporting values of interest")

        if os.path.isfile("%s" %(self.voi)):
            #Determine my interests
            with open(self.voi) as f:
                content = f.readlines()
                content = [x.strip() for x in content] #Remove Whitespace
            #Read the measures that have been pre-derived   
            measures={}
            
            measures["PatientVisit"]=self.path           
            
            if os.path.isfile("%s/crush/tracts.txt" %(self.tractographypath)):
                with open("%s/crush/tracts.txt" %(self.tractographypath)) as fMeasure:
                    for line in fMeasure:
                        nvp=line.split("=")                        
                        measures[nvp[0]]=nvp[1]



                
                row=[]
                row.append(os.path.split(os.path.dirname(self.path))[1])
                row.append(self.VisitId)

                #self.data['key'].append
                
                for cell in content:
                    if cell in measures:
                        row.append(measures[cell].strip())
                        
                    #       self.data[(os.path.split(os.path.dirname(self.path))[1])][self.VisitId][cell]=measures[cell].strip()
                    else:
                        row.append("")                              
                print(",".join(row))
    