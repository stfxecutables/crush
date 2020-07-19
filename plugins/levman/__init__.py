import os, sys,inspect
import subprocess
import numpy as np
import re
import time
import datetime
import uuid
from basecrush.ux import MsgUser
import nibabel as nib
from shutil import copyfile
from multiprocessing import Pool,cpu_count
import csv as csvModule
import warnings
from collections import defaultdict
import json
import gzip
import shutil
import configparser
import psycopg2


PipelineId="levman"

def run(visit):
       
    P = Pipeline(visit)
    P.PipelineId=PipelineId
    P.run()

   
def csv(Patients,**kwargs):  

    if ('metadata' in kwargs):
        Metadata = kwargs['metadata']
        headerNames = Metadata['Header']

    #The feature metadata file should have the format 
    # ParcellationId,Label,asymetry counterpart,Left or Right,White or Grey,Common Name
    #e.g. 3035,wm-lh-insula,4035,Left,White Matter,Insula
    #Use hashtag to comment a line
    Features = {}
    i=1
    segmentMap="%s/%s" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),"segmentMap.csv")
    with open(segmentMap) as fin:
        reader=csvModule.reader(fin, skipinitialspace=True, quotechar="'")
        p = re.compile('^ *#')   # if not commented          
        for row in reader:                
            if(not p.match(row[0])): 
                if row[0] not in Features:
                    Features[row[0]]={}
                #ParcellationId,Label,asymetry counterpart,Left or Right,White or Grey,Common Name
                try:                    
                    Features[row[0]]['ROI']=row[0]
                    Features[row[0]]['ROI Label']=row[1]
                    Features[row[0]]['Asymmetry Counterpart']=row[2]
                    Features[row[0]]['White Grey Counterpart']=row[3]
                    Features[row[0]]['Left or Right']=row[4]
                    Features[row[0]]['White or Grey']=row[5]
                    Features[row[0]]['Common Name']=row[6]                    
                except:
                    print("Potentially malformed segmentMap.csv on line %s of %s" %(i, segmentMap))
                    exit()
            i=i+1
    #Print CSV Header
    row=[]
    row.append("PatientId")
    row.append("VisitId")
    if ('metadata' in kwargs):
        for meta_i in range(2,len(headerNames)):
            meta=headerNames[meta_i]
            row.append(meta)  

    row.append('ROI')
    row.append('ROI Label')
    #row.append('Asymmetry Counterpart')
    row.append('Left or Right')
    row.append('White or Grey')
    row.append('Common Name')
    row.append('ROI END')
    row.append('ROI END Label')        
    row.append('Method')

    measureNames = ['NumTracts',
        'TractsToRender',
        'LinesToRender',
        'MeanTractLen',
        'MeanTractLen_StdDev',
        'VoxelSizeX',
        'VoxelSizeY',
        'VoxelSizeZ',
        'meanFA',
        'stddevFA',
        'meanADC',
        'stddevADC',
        'NumTracts-asymidx',
        'TractsToRender-asymidx',
        'LinesToRender-asymidx',
        'MeanTractLen-asymidx',
        'MeanTractLen_StdDev-asymidx',
        'VoxelSizeX-asymidx',
        'VoxelSizeY-asymidx',
        'VoxelSizeZ-asymidx',
        'meanFA-asymidx',
        'stddevFA-asymidx',
        'meanADC-asymidx',        
        'stddevADC-asymidx']

    for mn in measureNames:            
        row.append(mn)
  
    print(",".join(row))

    #SET up iterator for each row

    Segments=[]
    tasks=[]
    methods=[]  #Methods represents the possible ROI switches to trackvis, e.g methods = ["roi","roi_end"]
    methodFile="%s/%s" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),"methods.txt")
    with open(methodFile) as fin:
        reader=csvModule.reader(fin, skipinitialspace=True, quotechar="'")
        p = re.compile('^ *#')   # if not commented          
        for row in reader:
            if(not p.match(row[0])):                    
                methods.append(row[0])  

    i=1
    segmentMap="%s/%s" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),"segmentMap.csv")
    with open(segmentMap) as fin:
        reader=csvModule.reader(fin, skipinitialspace=True, quotechar="'")
        p = re.compile('^ *#')   # if not commented          
        for row in reader:            
            if(not p.match(row[0])): 
                Segments.append({'roi':row[0],'roiname':row[1],'asymmetry':row[2]})
            i=i+1

 
    #Print CSV Data
    for p in Patients:
        for v in p.Visits:
            
            measurements = v.GetMeasurements()  
                        
            #=====================================================
            asymMeasuresToAdd = {}
            for m in measurements:
                if len(m)>8 and m[-8] != "-asymidx":
                    m0 = re.match("^"+PipelineId+"\/(\w+)-(\w+)-(\w+)-(\w+)",m)
                    
                    if m0:
                        l_roi = m0.group(1)
                        l_roiE = m0.group(2)
                        l_method = m0.group(3)
                        l_measure = m0.group(4)

                        l_roiC=""
                        l_roiEC=""

                        #print("%s, %s" %(l_roi,l_roiE))
                        for s in Segments:                        
                            if s['roi']==l_roi:                            
                                l_roiC = s['asymmetry']
                            if s['roi']==l_roiE:
                                l_roiEC = s['asymmetry']

                        asymCounterpart = PipelineId+"/%s-%s-%s-%s" %(l_roiC,l_roiEC,l_method,l_measure)                    
                        if asymCounterpart in measurements:
                            if v.is_number(measurements[m]) and v.is_number(measurements[asymCounterpart]) and float(measurements[asymCounterpart]) != 0:
                                asymIdx=float(measurements[m]) / float(measurements[asymCounterpart])                            
                                asymMeasuresToAdd["%s-asymidx" %(m)] = asymIdx

            #print(asymMeasuresToAdd)
            #return
            for newm in asymMeasuresToAdd:
                if v.is_number(str(asymMeasuresToAdd[newm])):
                    measurements[newm]=str(asymMeasuresToAdd[newm])


            #===================================================== 
            
            row=[]                
            row.append(p.PatientId)            
            row.append(v.VisitId)

            if ('metadata' in kwargs):
                for meta_i in range(2,len(headerNames)):
                    meta=headerNames[meta_i]
                    if p.PatientId in Metadata['Rows'] and v.VisitId in Metadata['Rows'][p.PatientId] and meta in Metadata['Rows'][p.PatientId][v.VisitId] :
                        row.append(Metadata['Rows'][p.PatientId][v.VisitId][meta])
                    else:
                        row.append("")
            
            ## A measurement root represents one intersection of ROI x ROI x Method
            ## For example 0002-0004-roi_end
            ## There will be one CSV row per root, with measures for columns

            measurementRoots = []
            for s in Segments:
                segment=s['roi']
                segmentName=s['roiname']                                            
                for c in Segments:
                    counterpart=c['roi']
                    counterpartName=c['roiname']                               
                    if (segment!=counterpart):                                         
                        for method in methods:                    
                            if segment != counterpart:                        
                                t = segment+'-'+counterpart+'-'+method                       
                                measurementRoots.append(t.strip())
            
           
            for m in measurementRoots:     #For all rows                             
                row=[]                
                row.append(p.PatientId)            
                row.append(v.VisitId)

                if ('metadata' in kwargs): #Write out any metadata
                    for meta_i in range(2,len(headerNames)):
                        meta=headerNames[meta_i]
                        if p.PatientId in Metadata['Rows'] and v.VisitId in Metadata['Rows'][p.PatientId] and meta in Metadata['Rows'][p.PatientId][v.VisitId] :
                            row.append(Metadata['Rows'][p.PatientId][v.VisitId][meta])
                        else:
                            row.append("")

                #What do we know about this ROI?
                m0 = re.match("^(\w+)-(\w+)-(\w+)",m)
                if m0 and m0.group(1) in Features:                         
                    roi=Features[m0.group(1)]['ROI']
                    roiLabel=Features[m0.group(1)]['ROI Label']
                    roiEnd=Features[m0.group(2)]['ROI']
                    roiEndLabel=Features[m0.group(2)]['ROI Label']
                    #asymIdx=Features[m0.group(1)]['Asymmetry Counterpart']
                    lw=Features[m0.group(1)]['Left or Right']
                    wg=Features[m0.group(1)]['White or Grey']                       
                    cn=Features[m0.group(1)]['Common Name']
                    method=m0.group(3)
                    #measure=m0.group(4)
                else:
                    roi=m0.group(1)
                    roiLabel=""
                    roiEnd=m0.group(2)
                    roiEndLabel=""
                    asymIdx=""
                    lw=""
                    wg=""
                    cn=""
                    method=m0.group(3)
                    #measure=m0.group(4)

                row.append(roi)
                row.append(roiLabel)
                #row.append(asymIdx)
                row.append(lw)
                row.append(wg)
                row.append(cn)
                row.append(roiEnd)
                row.append(roiEndLabel)                    
                row.append(method)
                #row.append(measure)

                for mn in measureNames:
                    if PipelineId+'/'+m+'-'+mn in measurements:
                        row.append(measurements[PipelineId+'/'+m+'-'+mn])
                    else:
                        row.append("")

                print(",".join(row))    


class Pipeline:
   
    def __init__(self,object): 
        self.PipelineId = "levman"

        config = configparser.ConfigParser() 
        config.read(os.path.join(os.path.dirname(__file__), 'levman.ini'))             
        #config.read('~/projects/crush/plugins/levman/levman.ini')
        #config.sections()
        self.dbname=config['DATABASE']['dbname']
        self.dbuser=config['DATABASE']['user']
        self.dbpass=config['DATABASE']['password']
            
        self.visit = object
        self.eddyCorrectedData=""

        self.Segments = []#{}

        i=1
        segmentMap="%s/%s" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),"segmentMap.csv")
        with open(segmentMap) as fin:
            reader=csvModule.reader(fin, skipinitialspace=True, quotechar="'")
            p = re.compile('^ *#')   # if not commented          
            for row in reader:
                #print("%s,%s" %(i,row))
                if(not p.match(row[0])): 
                    self.Segments.append({'roi':row[0],'roiname':row[1],'asymmetry':row[2]})
                i=i+1
        '''
        self.VisitId=object.VisitId
        self.path=object.path
        self.rebuild=object.rebuild
        self.voi=object.voi        
        self.recrush=object.recrush
        self.fixmissing=object.fixmissing        
        self.maxcores=object.maxcores 
        self.data = object.data
        self.PatientId=object.PatientId        
        self.disable_log=object.disable_log
        self.ReconComplete=object.ReconComplete
        self.MeasurementComplete=object.MeasurementComplete   
        self.Segments = object.Segments  
        ''' 
        MsgUser.message("##############################################...")
        MsgUser.message("Levman pipeline initialized for patient visit: "+ object.path)
        MsgUser.message("##############################################...")
            
    def run(self):  

        self.dbtest()
        return;        
        print("%s:%s" %("mgz2nifti started:",datetime.datetime.now()))
        self.mgz2nifti()      
#        self.flirt()
#        return
        print("%s:%s" %("eddy_correct started:",datetime.datetime.now()))  
        self.eddy_correct()
        print("%s:%s" %("hardi_mat started:",datetime.datetime.now()))
        self.hardi_mat()            
        print("%s:%s" %("odf recon started:",datetime.datetime.now()))
        self.odf_recon()
        print("%s:%s" %("odf tracker started:",datetime.datetime.now()))
        self.odf_tracker()
        print("%s:%s" %("flirt started:",datetime.datetime.now()))
        self.flirt()
    

        print("%s:%s" %("tract_transform started:",datetime.datetime.now()))
        self.tract_transform()
        print("%s:%s" %("dti_recon started:",datetime.datetime.now()))
        self.dti_recon()
        print("%s:%s" %("dti_tracker started:",datetime.datetime.now()))
        self.dti_tracker()
        print("%s:%s" %("parcellation started:",datetime.datetime.now()))
        self.parcellate()
        print("%s:%s" %("track_vis started:",datetime.datetime.now()))
        self.track_vis()


    def unicode_csv_reader(utf8_data, dialect=csvModule.excel, **kwargs):
            csv_reader = csvModule.reader(utf8_data, dialect=dialect, **kwargs)
            for row in csv_reader:
                yield [unicode(cell, 'utf-8') for cell in row]

    def dbtest(self):
        try:
            conn=psycopg2.connect("dbname='%s' user='%s' password='%s'" %(self.dbname,self.dbuser,self.dbpass))
            print("Connected to %s" %(self.dbname))
        except:
            print("Failed to connect to [%s].  Check .ini file in plugin" %(self.dbname))
            return
        cur=conn.cursor()

        cur.execute("""
        SELECT EXISTS(SELECT 1 FROM information_schema.tables 
              WHERE table_catalog='%s' AND 
                    table_schema='%s' AND 
                    table_name='crush_measures')""" %(self.dbname,self.dbuser)
        );
        tableExists = cur.fetchone()[0]
        
        if (tableExists):
            print("crush_measures table found in %s" %(self.dbname))            
        else:

            cur.execute("""
               Create table %s.crush_measures (
                   roi_start varchar(4),
                   roi_end varchar(4),
                   method varchar(10),
                   measure varchar(20),
                   value varchar(30),
                 unique(roi_start,roi_end,method,measure));
            """ %(self.dbuser))
            conn.commit();
            print("crush_measures table created in %s" %(self.dbname))

        cur.execute("""
            INSERT INTO %s.crush_measures(roi_start,roi_end,method,measure,value)
            VALUES('%s','%s','%s','%s','%s')
            on conflict(roi_start,roi_end,method,measure)
            do
              update set value=excluded.value
            """ %(self.dbuser,'0002','0004','roi','meas','12'))    
        conn.commit()

    def MeasurementAudit(self):     
        '''
        This routine is used as a recovery tool in the event the processing failed.
        Since this pipeline takes so long to render we have to anticipate failures. 
        This function looks for all measures that should be there to determine 
        if there is anything missing.
        '''   
        tasks = []

        for s in self.Segments:
            segment=s['roi']
            segmentName=s['roiname']                                            
            for c in self.Segments:
                counterpart=c['roi']
                counterpartName=c['roiname']                               
                if (segment!=counterpart and segment<counterpart):                        
                    methods=[]  #Methods represents the possible ROI switches to trackvis, e.g methods = ["roi","roi_end"]
                    methodFile="%s/%s" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),"methods.txt")
                    with open(methodFile) as fin:
                        reader=csvModule.reader(fin, skipinitialspace=True, quotechar="'")
                        p = re.compile('^ *#')   # if not commented          
                        for row in reader:
                            if(not p.match(row[0])):                    
                                methods.append(row[0])                    
                    for method in methods:
                        #print("Rendering segment %s counterpart %s method %s" %(segment, counterpart, method))
                        if segment != counterpart:
                            completeInd = self.MeasurementAudit_worker(segment,counterpart,method)
                            if completeInd:
                                #Get into global data array
                                for m in completeInd:
                                    self.visit.SetValue(self.PipelineId,m,completeInd[m])
                                    #self.visit.data[self.visit.PatientId][self.visit.VisitId][m] = completeInd[m]

                                MsgUser.ok("Measurement complete: %s %s %s" %(segment,counterpart,method))
                                
                            else:                                
                                MsgUser.failed("Measurement incomplete: %s %s %s" %(segment,counterpart,method))
                            tasks.append(completeInd)
        l=len(tasks)    
        positives = 0    
        for t in tasks:
            if t:
                positives += 1

        print("%s/%s is %s percent complete.  %s positives" %(self.visit.PatientId, self.visit.VisitId,positives/l*100,positives))
        return completeInd

    def MeasurementAudit_worker(self,segment,counterpart,method):

        calcs={}

        calcsJson = "%s/crush/%s/calcs-%s-%s-%s.json" % (self.visit.tractographypath,segment,segment,counterpart,method)
        if os.path.isfile(calcsJson):
            with open(calcsJson, 'r') as f:
                calcs = json.loads(f.read())
                return calcs
        else:
            #Check for and Fix legacy structure and put JSON in segment folders
            calcsOldJson = "%s/crush/calcs-%s-%s-%s.json" % (self.visit.tractographypath,segment,counterpart,method)
            if os.path.isfile(calcsOldJson):
                with open(calcsOldJson, 'r') as f:
                    calcs = json.loads(f.read())
                    if not os.path.isdir("%s/crush/%s" % (self.visit.tractographypath,segment)):
                        os.mkdir("%s/crush/%s" % (self.visit.tractographypath,segment))
                    os.rename(calcsOldJson,calcsJson)
                    return calcs

        l_NumTracts = False
        l_TractsToRender = False
        l_LinesToRender = False
        l_MeanTractLen = False
        l_MeanTractLen_StdDev = False
        l_VoxelSizeX = False
        l_VoxelSizeY = False
        l_VoxelSizeZ = False
        l_meanFA = False
        l_stddevFA = False
        l_meanADC = False
        l_stddevADC = False

        p = "%s-%s-%s-NumTracts" %(segment,counterpart,method)                          
        if(p in self.visit.data[self.visit.PatientId][self.visit.VisitId]):
            l_NumTracts=True            
            calcs[p]= self.visit.GetValue(self.PipelineId,p)
            #self.visit.data[self.visit.PatientId][self.visit.VisitId][p]

        p = "%s-%s-%s-TractsToRender" %(segment,counterpart,method)                    
        if(p in self.visit.data[self.visit.PatientId][self.visit.VisitId]):
            l_TractsToRender=True     
            calcs[p] = self.visit.GetValue(self.PipelineId,p)
            #self.visit.data[self.visit.PatientId][self.visit.VisitId][p]          

        p = "%s-%s-%s-LinesToRender" %(segment,counterpart,method)                    
        if(p in self.visit.data[self.visit.PatientId][self.visit.VisitId]):
            l_LinesToRender=True                        
            calcs[p] = self.visit.GetValue(self.PipelineId,p)
            #self.visit.data[self.visit.PatientId][self.visit.VisitId][p]          
            
        p = "%s-%s-%s-MeanTractLen" %(segment,counterpart,method)                    
        if(p in self.visit.data[self.visit.PatientId][self.visit.VisitId]):
            l_MeanTractLen=True     
            calcs[p] = self.visit.GetValue(self.PipelineId,p)
            # self.visit.data[self.visit.PatientId][self.visit.VisitId][p]          

        p = r"%s-%s-%s-MeanTractLen_StdDev" %(segment,counterpart,method)                    
        if(p in self.visit.data[self.visit.PatientId][self.visit.VisitId]):
            l_MeanTractLen_StdDev=True                                                
            calcs[p] = self.visit.GetValue(self.PipelineId,p)
            #self.visit.data[self.visit.PatientId][self.visit.VisitId][p]          

        p = "%s-%s-%s-VoxelSizeX" %(segment,counterpart,method)                    
        if(p in self.visit.data[self.visit.PatientId][self.visit.VisitId]):
            l_VoxelSizeX=True                        
            calcs[p] = self.visit.GetValue(self.PipelineId,p)
            #self.data[self.PatientId][self.VisitId][p]          

        p = "%s-%s-%s-VoxelSizeY" %(segment,counterpart,method)                    
        if(p in self.visit.data[self.visit.PatientId][self.visit.VisitId]):
            l_VoxelSizeY=True                        
            calcs[p] = self.visit.GetValue(self.PipelineId,p)
            #self.data[self.PatientId][self.VisitId][p]          

        p = "%s-%s-%s-VoxelSizeZ" %(segment,counterpart,method)                    
        if(p in self.visit.data[self.visit.PatientId][self.visit.VisitId]):
            l_VoxelSizeZ=True                        
            calcs[p] = self.visit.GetValue(self.PipelineId,p)
            #self.data[self.PatientId][self.VisitId][p]          

        p = "%s-%s-%s-meanFA" %(segment,counterpart,method)                    
        if(p in self.visit.data[self.visit.PatientId][self.visit.VisitId]):
            l_meanFA=True                        
            calcs[p] = self.visit.GetValue(self.PipelineId,p)
            #self.data[self.PatientId][self.VisitId][p]          

        p = "%s-%s-%s-stddevFA" %(segment,counterpart,method)                    
        if(p in self.visit.data[self.visit.PatientId][self.visit.VisitId]):
            l_stddevFA=True                        
            calcs[p] = self.visit.GetValue(self.PipelineId,p)
            #self.data[self.PatientId][self.VisitId][p]          

        p = "%s-%s-%s-meanADC" %(segment,counterpart,method)                    
        if(p in self.visit.data[self.visit.PatientId][self.visit.VisitId]):
            l_meanADC=True                        
            calcs[p] = self.visit.GetValue(self.PipelineId,p)
            #self.data[self.PatientId][self.VisitId][p]          

        p = "%s-%s-%s-stddevADC" %(segment,counterpart,method)                    
        if(p in self.visit.data[self.visit.PatientId][self.visit.VisitId]):
            l_stddevADC=True     
            calcs[p] =self.visit.GetValue(self.PipelineId,p)
            #self.data[self.PatientId][self.VisitId][p]          

        if(l_NumTracts and l_TractsToRender and l_LinesToRender and l_MeanTractLen
            and l_MeanTractLen_StdDev and l_VoxelSizeX and l_VoxelSizeY and l_VoxelSizeZ
            and l_meanFA and l_stddevFA and l_meanADC and l_stddevADC):

            #We have everything in the tract file
            return calcs
        else:
            #We don't have everything we need from the tract file
            #Lets see if we cached it the last time we processed this sample
            
            
            #else:
                #Can't find any residue - looks like this is a new calc
            return {}
  
    def mgz2nifti(self):  
        MsgUser.bold("mgz2nifti")
        if self.visit.rebuild!=True and os.path.isfile("%s/mri/brainmask.nii" % (self.visit.freesurferpath)):
            self.visit.NiftiComplete=True
            MsgUser.skipped("All Nifti files exist")
        else:
            MsgUser.warning("\tNifti Incomplete, rendering nii files...")
                    
            mgzFiles=['aseg','aparc+aseg', 'aparc.a2009s+aseg', 'lh.ribbon', 'rh.ribbon', 'nu', 'orig', 'ribbon', 'wm.asegedit', 'wm', 'wm.seg', 'brain', 'brainmask']
        
            for mgz in mgzFiles:
                if os.path.isfile("%s/mri/%s.nii" % (self.visit.freesurferpath,mgz)) :
                    MsgUser.skipped("\t%s.nii exists" % (mgz))
                else:
                
                    MsgUser.message("Create or replace %s.nii" % (mgz))
                    ret = subprocess.call(['mri_convert','-rt','nearest','-nc','-ns','1',"%s/mri/%s.mgz" %(self.visit.freesurferpath,mgz),"%s/mri/%s.nii" % (self.visit.freesurferpath,mgz)])
                    if ret !=0:
                        MsgUser.failed("mri_convert failed with error")
                        exit()
    def eddy_correct(self):
        MsgUser.bold("eddy_correct")

        #eddy_correct ~/HealthyTractography/%s/%s/DTI35.nii ~/HealthyTractography/%s/%s/DTI35_eddy.nii 0
        #if os.path.isfile("%s/DTI35_eddy.nii.gz" %(self.visit.tractographypath)):
        if self.visit.rebuild!=True  and os.path.isfile("%s/data.nii.gz" %(self.visit.tractographypath)):
            self.eddyCorrectedData="%s/data.nii" %(self.visit.tractographypath)
            MsgUser.skipped("eddy_correct output exists [%s/data.nii.gz]" %(self.visit.tractographypath))

        else:
            #Removed June 2020 - not sure what I was thinking, leaving in comments for now.
            # #dtifit -k data.nii.gz -o dti -m nodif_brain_mask.nii.gz -r bvecs -b bvals
            # cmdArray=["dtifit","-k","data.nii.gz", "-o","dti","-m","nodif_brain_mask.nii.gz" ,"-r","bvecs","-b","bvals"]
            # print(cmdArray)
            # subprocess.call(cmdArray,cwd=self.visit.diffusionpath)
    
            # if os.path.isfile("%s/dti_FA.nii.gz" %(self.visit.diffusionpath)):# and os.path.isfile("%s/DTI35_eddy.nii.gz" %(self.visit.diffusionpath)):
            #     os.rename("%s/dti_FA.nii.gz" %(self.visit.diffusionpath),"%s/DTI.nii.gz" %(self.visit.tractographypath))
            #     #os.rename("%s/DTI35_eddy.nii.gz" %(self.visit.diffusionpath),"%s/DTI35_eddy.nii.gz" %(self.visit.tractographypath))

            if self.visit.SourceTaxonomy=="BCH":
                cmdArray=["eddy_correct","%s/data.nii.gz" % (self.visit.diffusionpath),"%s/data.nii.gz" % (self.visit.tractographypath),"0"]                
                ret = subprocess.call(cmdArray)
                if ret !=0:
                    MsgUser.failed("eddy_correct failed with error")
                    exit()   
                self.eddyCorrectedData="%s/data.nii.gz" %(self.visit.tractographypath)             
                MsgUser.ok("eddy_correct Completed")
            elif self.visit.SourceTaxonomy=="HCP":
                #HCP data is already eddy corrected
                
                os.rename("%s/data.nii.gz" %(self.visit.diffusionpath),"%s/data.nii.gz" %(self.visit.tractographypath))
                with gzip.open("%s/data.nii.gz" %(self.visit.tractographypath), 'rb') as f_in:
                    with open("%s/data.nii" %(self.visit.tractographypath), 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)

               
                self.eddyCorrectedData=self.visit.tractographypath+"/data.nii"

    #  else:


    #         #eddy_correct dti_FA.nii.gz DTI35_eddy.nii.gz 0
    #         cmdArray=["eddy_correct","%s/DTI35.nii.gz" %(self.visit.tractographypath),"%s/DTI35_eddy.nii.gz"%(self.visit.tractographypath) ,"0"]
    #         print(cmdArray)
    #         subprocess.call(cmdArray,cwd=self.visit.tractographypath)
            
    def createGradientMatrix(self):

        a = zip(*csvModule.reader(open("%s/bvecs" %(self.visit.diffusionpath), "rt")))
        csvModule.writer(open("%s/bvecs2gradientMatrix.txt" %(self.visit.tractographypath), "wt")).writerows(a)

        
    def createGradientMatrixNHDR(self):

        if("NHDRCONVERSION" in os.environ):
            #nhdr_write.py --nifti data.nii.gz --bval bvals --bvec bvecs --nhdr davegradient.nhdr
            cmdArray=["python","%s/nhdr_write.py" %(os.environ["NHDRCONVERSION"]),"--nifti",
              "%s/data.nii.gz" %(self.visit.diffusionpath),
              "--bval","%s/bvals" %(self.visit.diffusionpath),
              "--bvec","%s/bvecs" %(self.visit.diffusionpath),
              "--nhdr","%s/gradient_table.nhdr" %(self.visit.tractographypath)
              ]
            print(cmdArray)
            subprocess.call(cmdArray)
            #Convert NHDR to text

        else:
            MsgUser.failed("NHDRCONVERSION variable not set.  Please set to installation path for https://github.com/pnlbwh/conversion/") 
            exit()

            
        
    def hardi_mat(self):
        MsgUser.bold("hardi_mat")
        if self.visit.rebuild!=True and os.path.isfile("%s/temp_mat.dat" %(self.visit.tractographypath)):
            MsgUser.skipped("hardi_mat output exists")
        else:
            defaultGradientMatrix ="%s/%s" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),"gradientMatrix_HCP.txt")
            if(not os.path.isfile("%s/hcp_gradient_table_from_data_dictionary_3T.csv"%(self.visit.tractographypath))):
                self.createGradientMatrix()

            cmdArray=["hardi_mat","%s/hcp_gradient_table_from_data_dictionary_3T.csv" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))),"%s/temp_mat.dat" % (self.visit.tractographypath), "-ref",self.eddyCorrectedData,"-oc"]
            print(cmdArray)
            ret = subprocess.call(cmdArray)

            if ret !=0:
                        MsgUser.failed("hardi_mat failed with error")
                        exit()
            else:
                MsgUser.ok("HARDIReconstruction Completed")
            

    def odf_recon(self):
        MsgUser.bold("odf_recon")
        #output: DTI35_Recon_max.nii.gz
        if self.visit.rebuild!=True  and os.path.isfile("%s/DTI_Recon_max.nii.gz" %(self.visit.tractographypath)):
            #odf_, max_, dwi_, b0 files should exist
            MsgUser.skipped("odf_recon output exists")
        else:
            
            #cmdArray=["odf_recon","%s/DTI35_eddy.nii.gz" %(self.visit.tractographypath),"31","181","%s/DTI35_Recon" %(self.visit.tractographypath),"-b0", "5","-mat","%s/temp_mat.dat" %(self.visit.tractographypath),"-p","3","-sn", "1", "-ot", "nii.gz"]
            #~/bin/odf_recon data.nii 125 181 DTI_Recon -b0 1 -p 3 -sn 1 -ot nii -mat ~/projects/def-dmattie/HCP/100307/T1w/Diffusion/temp_mat.dat
            cmdArray=["odf_recon",self.eddyCorrectedData,"270","181","%s/DTI_Recon" %(self.visit.tractographypath),"-b0", "18","-mat","%s/temp_mat.dat" %(self.visit.tractographypath),"-p","3","-sn", "1", "-ot", "nii.gz"]
            print(cmdArray)
            ret = subprocess.call(cmdArray)
            if ret !=0:
                MsgUser.failed("odf_recon failed with error")
                exit()

            MsgUser.ok("odf_recon Completed")
            
    def odf_tracker(self):
        MsgUser.bold("odf_tracker")
        #output: DTI35_Recon_max.nii.gz
        
        if (self.visit.rebuild!=True and os.path.isfile("%s/DTI_Recon_dwi.nii.gz" %(self.visit.tractographypath)) == False):
            MsgUser.failed("odf_tracker cannot be completed, odf_recon did not finish, missing DTI_Recon files")
            return
            
        if self.visit.rebuild!=True  and os.path.isfile("%s/DTI_preReg.trk" %(self.visit.tractographypath)):
            #odf_, max_, dwi_, b0 files should exist
            MsgUser.skipped("odf_tracker output exists")
        else:
            #cmdArray=["odf_tracker","%s/DTI_Recon" %(self.visit.tractographypath),"%s/DTI_preReg.trk" %(self.visit.tractographypath),"-at","45","-m", "%s/DTI_Recon_dwi.nii.gz" %(self.visit.tractographypath),"-it","nii.gz"]
            cmdArray=["odf_tracker","%s/DTI_Recon" %(self.visit.tractographypath),"%s/DTI_preReg.trk" %(self.visit.tractographypath),"-at","35","-m", "%s/DTI_Recon_dwi.nii.gz" %(self.visit.tractographypath),"-it","nii.gz"]
            print(cmdArray)
            ret = subprocess.call(cmdArray)
            if ret !=0:
                MsgUser.failed("odf_tracker failed with error")
                exit()

            MsgUser.ok("odf_tracker Completed")
            
    def flirt(self):
        MsgUser.bold("flirt")
        #output: RegTransform4D
        

        if self.visit.rebuild!=True  and os.path.isfile("%s/RegTransform4D" %(self.visit.tractographypath)):        
            MsgUser.skipped("flirt output exists")            
        else:
            #flirt -in ./DTI35_eddy.nii.gz -ref ./brainmask.nii -omat ./RegTransform4D
            cmdArray=["flirt","-in",self.eddyCorrectedData,"-ref","%s/mri/brainmask.nii" %(self.visit.freesurferpath),"-omat","%s/RegTransform4D" %(self.visit.tractographypath),"-o","%s/data-flirtout.nii" %(self.visit.tractographypath)]
            print(cmdArray)
            ret = subprocess.call(cmdArray)
            if ret !=0:
                MsgUser.failed("flirt failed with error")
                exit()
         
            MsgUser.ok("flirt Completed")
            
    def tract_transform(self):
        MsgUser.bold("tract_transform")
        #output: DTI35_postReg.trk
        if self.visit.rebuild!=True  and os.path.isfile("%s/DTI_postReg.trk" %(self.visit.tractographypath)):#TODO Need correct filename
            #odf_, max_, dwi_, b0 files should exist
            MsgUser.skipped("tract_transform output exists")
        else:
            #track_transform DTI35_preReg.trk DTI35_postReg.trk -src DTI35_Recon_dwi.nii.gz -ref brainmask.nii -reg RegTransform4D

            cmdArray=["track_transform","%s/DTI_preReg.trk" %(self.visit.tractographypath),"%s/DTI_postReg.trk" %(self.visit.tractographypath),"-src","%s/DTI_Recon_dwi.nii.gz"%(self.visit.tractographypath),"-ref", "%s/mri/brainmask.nii" %(self.visit.freesurferpath),"-reg","%s/RegTransform4D"%(self.visit.tractographypath)]
            print(cmdArray)
            ret = subprocess.call(cmdArray)
            if ret !=0:
                MsgUser.failed("track_transform failed with error")
                exit()

            MsgUser.ok("tract_transform Completed")
            
    def dti_recon(self):
        MsgUser.bold("dti_recon")
        if self.visit.rebuild!=True  and os.path.isfile("%s/DTI_Reg2Brain_fa.nii" %(self.visit.tractographypath)):#TODO we could test for all files to be sure
            #odf_, max_, dwi_, b0 files should exist
            MsgUser.skipped("dti_recon output exists")
        else:
            defaultGradientMatrix ="%s/%s" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),"hcp_gradient_table_from_data_dictionary_3T.csv")
            
            #cmdArray=["dti_recon","%s/DTI_eddy.nii.gz" %(self.visit.tractographypath),"%s/DTI_Reg2Brain" %(self.visit.tractographypath),"-gm",defaultGradientMatrix,"-b", "1000","-b0","5","-p","3","-sn","1","-ot","nii"]
            cmdArray=["dti_recon",self.eddyCorrectedData,"%s/DTI_Reg2Brain" %(self.visit.tractographypath),"-gm",defaultGradientMatrix,"-b", "3010","-b0","1","-p","3","-sn","1","-ot","nii"]
            print(cmdArray)
            ret = subprocess.call(cmdArray)
            if ret !=0:
                MsgUser.failed("dti_recon failed with error")
                exit()

            MsgUser.ok("dti_recon Completed")
            
        
    def dti_tracker(self):
        MsgUser.bold("dti_tracker")

        if self.visit.rebuild!=True  and os.path.isfile("%s/crush.trk" %(self.visit.tractographypath)):
            MsgUser.skipped("dti_tracker output exists")
        else:
            #dti_tracker DTI35_Reg2Brain DTI35_postReg.trk -m DTI35_Reg2Brain_fa.nii 0.15

            #cmdArray=["dti_tracker","%s/DTI35_Reg2Brain" %(self.visit.tractographypath),"%s/crush.trk" %(self.visit.tractographypath),"-m","%s/DTI35_Reg2Brain_fa.nii"%(self.visit.tractographypath),"-at","35","-m","%s/DTI35_Reg2Brain_dwi.nii" %(self.visit.tractographypath),"-it","nii"]
            cmdArray=["dti_tracker","%s/DTI_Reg2Brain" %(self.visit.tractographypath),"%s/crush.trk" %(self.visit.tractographypath),"-m","%s/DTI_Reg2Brain_fa.nii"%(self.visit.tractographypath),"-at","35","-m","%s/DTI_Reg2Brain_dwi.nii" %(self.visit.tractographypath),"-it","nii"]
            print(cmdArray)
            ret = subprocess.call(cmdArray)
            if ret !=0:
                MsgUser.failed("dti_tracker failed with error")
                exit()

            MsgUser.ok("dti_tracker Completed")

    def trackvis_create_nii(self,segment,counterpart,method):
        wmparcStart=f"{self.visit.tractographypath}/wmparc{segment}.nii"
        wmparcEnd=f"{self.visit.tractographypath}/wmparc{counterpart}.nii"
        if os.path.isfile(wmparcStart) and os.path.isfile(wmparcEnd):
            if self.visit.disable_log:
                trackvis = ["track_vis","%s/crush.trk" %(self.visit.tractographypath),"-%s"%(method),"%s/wmparc%s.nii" %(self.visit.tractographypath,segment),"-%s2" %(method),"%s/wmparc%s.nii" %(self.visit.tractographypath,counterpart),"-nr", "-ov","%s/crush/%s-%s-%s.nii" %(self.visit.tractographypath,segment,counterpart,method),"-disable_log"]
            else:
                trackvis = ["track_vis","%s/crush.trk" %(self.visit.tractographypath),"-%s"%(method),"%s/wmparc%s.nii" %(self.visit.tractographypath,segment),"-%s2" %(method),"%s/wmparc%s.nii" %(self.visit.tractographypath,counterpart),"-nr", "-ov","%s/crush/%s-%s-%s.nii" %(self.visit.tractographypath,segment,counterpart,method)]
            
            if not os.path.isfile("%s/crush/%s-%s-%s.nii" %(self.visit.tractographypath,segment,counterpart,method)):
                with open("%s/crush/%s/%s-%s-%s.nii.txt" %(self.visit.tractographypath,segment,segment,counterpart,method), "w") as track_vis_out:
                    proc = subprocess.Popen(trackvis, stdout=track_vis_out)
                    proc.communicate()
           
            with open ("%s/crush/%s/%s-%s-%s.nii.txt" %(self.visit.tractographypath,segment,segment,counterpart,method), "r") as myfile:
                data=myfile.read()               
            return data
        else:
            return ""

    def trackvis_cleanup_nii(self,segment,counterpart,method):

        nii = "%s/crush/%s-%s-%s.nii" %(self.visit.tractographypath,segment,counterpart,method)
        datafile = "%s/crush/%s/%s-%s-%s.nii.txt" %(self.visit.tractographypath,segment,segment,counterpart,method)
        oldcalcsfile = "%s/crush/calcs-%s-%s-%s.json" %(self.visit.tractographypath,segment,counterpart,method)
        
        if os.path.isfile(nii):
            os.unlink(nii) 
        
        if os.path.isfile(oldcalcsfile):
            print("Cleanup %s" %(oldcalcsfile))
            os.unlink(oldcalcsfile)             

                                                        

    def trackvis_worker(self,parr):#segment,counterpart,method):
        segment=parr[0]
        counterpart=parr[1]
        method=parr[2]

        calcs={}
                
        #track_vis ./DTI35_postReg_Threshold5.trk -roi_end ./wmparc3001.nii.gz -roi_end2 ./wmparc3002.nii.gz -nr
        
        #create wmparc#### if missing
        wmparcStart=f"{self.visit.tractographypath}/wmparc{segment}.nii"
        wmparcEnd=f"{self.visit.tractographypath}/wmparc{counterpart}.nii"
        #if not os.path.isfile("%s/wmparc%s.nii.gz" %(self.visit.tractographypath,segment)) and not os.path.isfile("%s/wmparc%s.nii.gz" %(self.visit.tractographypath,counterpart)):
        #    MsgUser.warning("%s/wmparc%s.nii.gz" %(self.visit.tractographypath,segment))

        #if os.path.isfile("%s/wmparc%s.nii.gz" %(self.visit.tractographypath,segment)) and os.path.isfile("%s/wmparc%s.nii.gz" %(self.visit.tractographypath,counterpart)):
        if os.path.isfile(wmparcStart) and os.path.isfile(wmparcEnd):

            render = True

            if self.visit.fixmissing:
                calcs = self.visit.MeasurementAudit_worker(segment,counterpart,method)
                if len(calcs)>0:
                    MsgUser.ok("Previous calculations detected for %s,%s,%s" %(segment,counterpart,method))
                    calcsJson = "%s/crush/%s/calcs-%s-%s-%s.json" % (self.visit.tractographypath,segment,segment,counterpart,method)

                    if not os.path.isdir("%s/crush/%s" % (self.visit.tractographypath,segment)):
                        os.mkdir("%s/crush/%s" % (self.visit.tractographypath,segment))

                    with open(calcsJson, "w") as calcs_file:
                        json.dump(calcs,calcs_file)                        
                        self.visit.trackvis_cleanup_nii(segment,counterpart,method)
                    #MsgUser.skipped("SKIPPING already calculated measures for %s-%s-%s" %(segment,counterpart,method))
                    return calcs
                else:
                    MsgUser.ok("Rendering missing measures for %s-%s-%s" %(segment,counterpart,method))

            
            data = self.trackvis_create_nii(segment,counterpart,method)
            
            print(data)
            m = re.search(r'Number of tracks: (\d+)', data)
            if m:
                NumTracts = m.group(1).strip()
            else:
                NumTracts = 0
            calcs["%s-%s-%s-NumTracts" %(segment,counterpart,method)]=NumTracts
            
            ############
            
            m = re.search(r'Number of tracks to render: (\d+)', data)
            if m:
                TractsToRender = m.group(1).strip()
            else:
                TractsToRender = 0
            calcs["%s-%s-%s-TractsToRender" %(segment,counterpart,method)]=TractsToRender
            
            ############
            
            m = re.search(r'Number of line segments to render: (\d+)', data)
            if m:
                LinesToRender = m.group(1).strip()
            else:
                LinesToRender = 0
            calcs["%s-%s-%s-LinesToRender" %(segment,counterpart,method)]=LinesToRender
            ############
            
            m = re.search(r'Mean track length: (\d+.\d+) \+\/- (\d+.\d+)', data)
            if m:
                MeanTractLen = m.group(1).strip()
                MeanTractLen_StdDev = m.group(2).strip()
            else:
                MeanTractLen = 0
                MeanTractLen_StdDev = 0
            
            calcs["%s-%s-%s-MeanTractLen" %(segment,counterpart,method)]=MeanTractLen
            calcs["%s-%s-%s-MeanTractLen_StdDev" %(segment,counterpart,method)]=MeanTractLen_StdDev
            ############
            
            m = re.search(r'Voxel size: (\d*[.,]?\d*) (\d*[.,]?\d*) (\d*[.,]?\d*)', data)
            if m:
                VoxelSizeX = m.group(1).strip()
                VoxelSizeY = m.group(2).strip()
                VoxelSizeZ = m.group(3).strip()
            else:
                VoxelSizeX = 0
                VoxelSizeY = 0
                VoxelSizeZ = 0

            calcs["%s-%s-%s-VoxelSizeX" %(segment,counterpart,method)]=VoxelSizeX
            calcs["%s-%s-%s-VoxelSizeY" %(segment,counterpart,method)]=VoxelSizeY
            calcs["%s-%s-%s-VoxelSizeZ" %(segment,counterpart,method)]=VoxelSizeZ

            
            #FA Mean
            meanFA=self.nonZeroMean("%s/DTI_Reg2Brain_fa.nii" %(self.visit.tractographypath),"%s/crush/%s-%s-%s.nii" %(self.visit.tractographypath,segment,counterpart,method))             
            calcs["%s-%s-%s-meanFA" %(segment,counterpart,method)]=meanFA
            
            #FA Std Dev
            stddevFA=self.nonZeroStdDev("%s/DTI_Reg2Brain_fa.nii" %(self.visit.tractographypath),"%s/crush/%s-%s-%s.nii" %(self.visit.tractographypath,segment,counterpart,method))         
            calcs["%s-%s-%s-stddevFA" %(segment,counterpart,method)]=stddevFA            
            
            #ADC Mean
            meanADC=self.nonZeroMean("%s/DTI_Reg2Brain_adc.nii" %(self.visit.tractographypath),"%s/crush/%s-%s-%s.nii" %(self.visit.tractographypath,segment,counterpart,method))         
            calcs["%s-%s-%s-meanADC" %(segment,counterpart,method)]=meanADC
            
            #ADC Std Dev
            stddevADC=self.nonZeroStdDev("%s/DTI_Reg2Brain_adc.nii" %(self.visit.tractographypath),"%s/crush/%s-%s-%s.nii" %(self.visit.tractographypath,segment,counterpart,method))       
            calcs["%s-%s-%s-stddevADC" %(segment,counterpart,method)]=stddevADC
            
            

        else:
            MsgUser.failed("Parcellation (wmparc####.nii) files missing (%s or %s)"%(segment,counterpart))
        
        # Cache CALCS to temp file because it's not written to tracts.txt until the join (after all ROIs finish)    
        
        if not os.path.isdir("%s/crush/%s" % (self.visit.tractographypath,segment)):
            os.mkdir("%s/crush/%s" % (self.visit.tractographypath,segment))

        calcsJson = "%s/crush/%s/calcs-%s-%s-%s.json" % (self.visit.tractographypath,segment,segment,counterpart,method)
        with open(calcsJson, "w") as calcs_file:
            json.dump(calcs,calcs_file)
            ############# CLEANUP #################
            self.trackvis_cleanup_nii(segment,counterpart,method)


        return calcs

    def track_vis(self):
        MsgUser.bold("track_vis")
        #output: crush.txt		
            
        #self.GetMeasurements()
        

        if self.visit.rebuild!=True  and os.path.isfile("%s/crush/tracts.txt" %(self.visit.tractographypath)):   
            
            if(self.visit.fixmissing!=True):
                if(self.visit.recrush):
                    print("Deleting previous crush output")
                    
                    folder = '%s/crush' %(self.visit.tractographypath)
                    for the_file in os.listdir(folder):
                        file_path = os.path.join(folder, the_file)
                        try:
                            if os.path.isfile(file_path):
                                os.unlink(file_path)        
                        except Exception as e:
                            print(e)
                else:
                    MsgUser.skipped("track_vis output exists")
                    return
            else:
                MsgUser.skipped("some track_vis output exists, I will crush anything missing")
                
        if not os.path.exists("%s/crush/" % (self.visit.tractographypath)):
            os.makedirs("%s/crush/" % (self.visit.tractographypath))

        
        #self.MeasurementAudit()
        #print(self.data)
        #return

        tasks = []

        methods=[]  #Methods represents the possible ROI switches to trackvis, e.g methods = ["roi","roi_end"]
        methodFile="%s/%s" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),"methods.txt")
        with open(methodFile) as fin:
            reader=csvModule.reader(fin, skipinitialspace=True, quotechar="'")
            p = re.compile('^ *#')   # if not commented          
            for row in reader:
                if(not p.match(row[0])):                    
                    methods.append(row[0])   

        for s in self.Segments:
            segment=s['roi']
            segmentName=s['roiname']                                            
            for c in self.Segments:
                counterpart=c['roi']
                counterpartName=c['roiname']                               
                if (segment!=counterpart):                                         
                    for method in methods:
                        #print("Rendering segment %s counterpart %s method %s" %(segment, counterpart, method))
                        if segment != counterpart:
                            MsgUser.ok("Setting up %s %s %s" %(segment,counterpart,method))                            
                            t = [segment,counterpart,method] 
                            print("Rendering %s against %s using method %s" % (segment,counterpart,method))
                            tasks.append(t)

        no_of_procs = cpu_count() 
        if(no_of_procs>self.visit.maxcores):
            no_of_procs = self.visit.maxcores
            
        print("Multiprocessing across %s async procs" %(no_of_procs))
                
        pool = Pool(no_of_procs)
        for t in tasks:
            pool.apply_async(self.trackvis_worker, (t,))            

        pool.close()
        pool.join()
        
        MsgUser.ok("@@@@  LETS JOIN IT ALL TOGETHER @@@@  ")

        self.MeasurementAudit()

        print("Patient measure count: %s" %(len(self.visit.data[self.visit.PatientId][self.visit.VisitId])))
        
        #visit.data = self.data
        self.visit.Commit()

        '''
        with open("%s/crush/tracts.txt" % (self.visit.tractographypath), "w") as crush_file:
            for m in self.data[self.PatientId][self.VisitId]: 
                if m[-8:] !="-asymidx":
                    crush_file.write("%s=%s\n" % (m,self.data[self.PatientId][self.VisitId][m]))
        '''
        
        self.visit.MeasurementComplete=True
        MsgUser.ok("track_vis Completed")


    def nonZeroMean(self,faFile,roiFile):
        
        if os.path.isfile(faFile) == False:        
            MsgUser.failed("%s is MISSING" %(faFile))
            return
        if os.path.isfile(roiFile) == False:        
            MsgUser.failed("%s is MISSING" %(roiFile))
            return

        imgFA = nib.load(faFile) #Untouched
        dataFA = imgFA.get_data()
        
        img = nib.load(roiFile)
        roiData = img.get_data()

        indecesOfInterest = np.nonzero(roiData)

        #I expect to see runtime warnings in this block, e.g. divide by zero
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)            
            mean =np.mean(dataFA[indecesOfInterest],dtype=np.float64)

        return mean
    def nonZeroStdDev(self,faFile,roiFile):
        
        if os.path.isfile(faFile) == False:        
            MsgUser.failed("%s is MISSING" %(faFile))
            return
        if os.path.isfile(roiFile) == False:        
            MsgUser.failed("%s is MISSING" %(roiFile))
            return

        imgFA = nib.load(faFile) #Untouched
        dataFA = imgFA.get_data()

        img = nib.load(roiFile)
        roiData = img.get_data()

        indecesOfInterest = np.nonzero(roiData)

        #I expect to see runtime warnings in this block, e.g. Degrees of freedom <= 0 for slice
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)            
            std =np.std(dataFA[indecesOfInterest],dtype=np.float64)

        return std
    
    def AddDerivedMeasures(self,visit):

        asymMeasuresToAdd = {}
        for m in visit.data[visit.PatientId][visit.VisitId]:
            if len(m)>8 and m[-8] != "-asymidx":
                m0 = re.match("^"+self.visit.PipelineId+"\/(\w+)-(\w+)-(\w+)-(\w+)",m)
                
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
                    if asymCounterpart in self.visit.data[self.visit.PatientId][self.visit.VisitId]:
                        if self.is_number(self.visit.data[self.visit.PatientId][self.visit.VisitId][m]) and self.visit.is_number(self.visit.visit.data[self.visit.PatientId][self.visit.VisitId][asymCounterpart]) and float(self.visit.data[self.visit.PatientId][self.visit.VisitId][asymCounterpart]) != 0:
                            asymIdx=float(self.visit.data[self.visit.PatientId][self.visit.VisitId][m]) / float(self.visit.data[self.visit.PatientId][self.visit.VisitId][asymCounterpart])                            
                            asymMeasuresToAdd["%s-asymidx" %(m)] = asymIdx
        for newm in asymMeasuresToAdd:
            if self.visit.is_number(str(asymMeasuresToAdd[newm])):
                Measurements[self.PipelineId+'/'+newm]=str(asymMeasuresToAdd[newm])
            
        ## End of derived measures
    def parcellate(self):
        #mri_extract_label $SUBJECTS_DIR/$1/T1w/$1/mri/wmparc.mgz $2 $SUBJECTS_DIR/$1/T1w/$1/mri/wmparc$2.mgz
        #mri_convert -rt nearest -nc -ns 1 $SUBJECTS_DIR/$1/T1w/$1/mri/wmparc$2.mgz $SUBJECTS_DIR/$1/T1w/$1/mri/wmparc$2.nii
        wmparc= f"{self.visit.freesurferpath}/mri/wmparc.mgz"
        for s in self.Segments:
            #print()
            segment= f"{s['roi']}"
            if (os.path.isfile(f"{self.visit.tractographypath}/wmparc{segment}.nii")):
                #print(f"FOUND: {self.visit.tractographypath}/wmparc{segment}.nii")
                continue
        
            cmdArray=["mri_extract_label",
                        wmparc,
                        segment,
                        f"{self.visit.tractographypath}/wmparc{segment}.mgz"]
                        
            print(cmdArray)
            ret = subprocess.call(cmdArray)
            if ret !=0:
                MsgUser.failed(f"Parcellation failed at segment {segment}")
                exit()

            cmdArray=["mri_convert",
                        "-rt",
                        "nearest",
                        "-nc",
                        "-ns",
                        "1",
                        f"{self.visit.tractographypath}/wmparc{segment}.mgz",
                        f"{self.visit.tractographypath}/wmparc{segment}.nii"
                        ]
                        
            print(cmdArray)
            ret = subprocess.call(cmdArray)
            if ret !=0:
                MsgUser.failed(f"Parcellation failed at segment {segment}")
                exit()  
            else:
                os.remove(f"{self.visit.tractographypath}/wmparc{segment}.mgz")         

        MsgUser.ok("Parcellation Completed")
