import os, sys,inspect,re
import basecrush.Patient
from basecrush.pluginloader import pluginloader
import csv
import math
from basecrush.ux import MsgUser

class Samples:
    Count=0
    
    
    def __init__(self,rootDir,force,voi,recrush,metadata,fixmissing,maxcores,disable_log,pipeline,csv,patient):
        self.Patients=[]
        self.force=force
        self.voi=voi
        self.recrush=recrush
        self.metadata=metadata
        self.fixmissing=fixmissing
        self.rootDir=rootDir
        self.maxcores=maxcores
        self.disable_log=disable_log
        self.pipeline=pipeline
        self.csv_flag=csv
        self.patient=patient

        dirs = os.listdir( rootDir )
        
        for file in dirs:
            patient_dir = "%s/%s" % (rootDir,file)
                   
            if os.path.isdir(patient_dir) and (self.patient is None or f"{self.patient}"==os.path.basename(patient_dir)):    
                print(f"Scanning {patient_dir}")            
                visits = os.listdir(patient_dir)
                for v in visits:
                    if(not os.path.islink("%s/%s" %(patient_dir,v))):
                        mri_dir = "%s/%s/Freesurfer/mri" % (patient_dir,v)
                        
                        if os.path.exists(mri_dir):
                            #print "%s/%s/mri" %(patient_dir,v)
                            #visit_dir = "%s/%s/01" % (rootDir,file)
                            #if os.path.exists(visit_dir): #assume if at least one visit then patient
                            self.Count+=1
                            patient=basecrush.Patient(patient_dir,self.force,self.voi,self.recrush,self.fixmissing,self.maxcores,self.disable_log,self.pipeline)
                            self.Patients.append(patient)
                        else:  #e.g. humanConnectome project doesn't have visits 100307/T1w/100307/mri
                            mri_dir = "%s/%s/%s/mri" % (patient_dir,v,file)
                            if os.path.exists(mri_dir):
                                #print "%s/%s/mri" %(patient_dir,v)
                                #visit_dir = "%s/%s/01" % (rootDir,file)
                                #if os.path.exists(visit_dir): #assume if at least one visit then patient
                                self.Count+=1
                                patient=basecrush.Patient(patient_dir,self.force,self.voi,self.recrush,self.fixmissing,self.maxcores,self.disable_log,self.pipeline)
                                self.Patients.append(patient)

                                   
    def csv(self):

        #Check for any patient metadata so we can augment output
        #The metadata file should have the format Patient,Visit,Attr1..AttrN
        #Metadata = {'Header':['Patient','Visit','Gender','Age']
        #            'Rows': {
        #                       '0001': {'01': {'Gender': 'Male', 'Age': '23.4759077245053'}},
        #                       '0002': {'01': {'Gender': 'Male', 'Age': '13.4354577245053'}},
        #           }

        Metadata = {} 
        if self.metadata and os.path.isfile(self.metadata):      
            with open(self.metadata, newline='') as f:
                reader = csv.reader(f)
                metaHeader = next(reader)
                Metadata['Header']=metaHeader
                
                rows={}

                for row in reader:   #iterate the metadata rows, add to dicitonary                    
                    for i in range(2,len(metaHeader)):    #iterate the cells of the row  
                        if row[0] not in rows:
                            rows[row[0]] = {}                        
                        if row[1] not in rows[row[0]]:
                            rows[row[0]][row[1]] = {}
                        
                        rows[row[0]][row[1]][metaHeader[i]]=row[i]
                
                Metadata['Rows']=rows
               

        if self.pipeline == None:
            MsgUser.warning("Pipeline plugin must be specified when extracting CSV")              
        else:
            for i in pluginloader.getPlugins():
                        
                if(self.pipeline==None or i["name"]==self.pipeline):                
                    plugin = pluginloader.loadPlugin(i)  
                    #try:
                    if(Metadata):
                        plugin.csv(self.Patients,metadata=Metadata)
                    else:
                        plugin.csv(self.Patients)
                    #except Exception:
                    #    print(Exception)
            
     

    def Report(self):

        #Check for any patient metadata so we can augment output
        #The metadata file should have the format Patient,Visit,Attr1..AttrN
        Metadata = {} 
        if self.metadata and os.path.isfile(self.metadata):      
            with open(self.metadata, newline='') as f:
                reader = csv.reader(f)
                metaHeader = next(reader)
                for row in reader:   #iterate the metadata rows, add to dicitonary                    
                    for i in range(2,len(metaHeader)):    #iterate the cells of the row  
                        if row[0] not in Metadata:
                            Metadata[row[0]] = {}                        
                        if row[1] not in Metadata[row[0]]:
                            Metadata[row[0]][row[1]] = {}
                        
                        Metadata[row[0]][row[1]][metaHeader[i]]=row[i]
        
        #The feature metadata file should have the format 
        # ParcellationId,Label,asymetry counterpart,Left or Right,White or Grey,Common Name
        #e.g. 3035,wm-lh-insula,4035,Left,White Matter,Insula
        #Use hastag to comment a line
        Features = {}
        i=1
        segmentMap="%s/%s" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),"segmentMap.txt")
        with open(segmentMap) as fin:
            reader=csv.reader(fin, skipinitialspace=True, quotechar="'")
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
                        Features[row[0]]['Left or Right']=row[3]
                        Features[row[0]]['White or Grey']=row[4]
                        Features[row[0]]['Common Name']=row[5]                    
                    except:
                        print("Potentially malformed segmentMap.txt on line %s of %s" %(i, segmentMap))
                        exit()
                i=i+1
        #Print CSV Header
        row=[]
        row.append("PatientId")
        row.append("VisitId")
        for meta_i in range(2,len(metaHeader)):
            meta=metaHeader[meta_i]
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
            #row.append(mn+" Asymmetry Index")
        #row.append('Measure Name')
        #row.append("Feature")
        #row.append("Measure")
        print(",".join(row))

        #Print CSV Data
        for p in self.Patients:
            for v in p.Visits:
                measurements = v.GetMeasurements()   
                #print(measurements)
                measurementRoots = []
                for m in measurements:
                    m0 = re.match("^(\w+)-(\w+)-(\w+)-(\w+)",m)
                    if m0:
                        r=m0.group(1)+"-"+m0.group(2)+"-"+m0.group(3)
                        if r.strip() not in measurementRoots:                              
                            measurementRoots.append(r.strip())                
                for m in measurementRoots:                                  
                    row=[]                
                    row.append(p.PatientId)            
                    row.append(v.VisitId)

                    for meta_i in range(2,len(metaHeader)):
                        meta=metaHeader[meta_i]
                        if p.PatientId in Metadata and v.VisitId in Metadata[p.PatientId] and meta in Metadata[p.PatientId][v.VisitId] :
                            row.append(Metadata[p.PatientId][v.VisitId][meta])
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
                        try:
                            #print("##"+m+'-'+mn)
                            #x = float(measurements[m+'-'+mn])
                            #if math.isnan(x):
                            #    row.append("")                                
                            #else:
                            if m + '-' + mn in measurements:
                                row.append(measurements[m + '-' + mn ])
                            else:
                                row.append("")
                        except:
                            row.append("Exception") #original                            
 
                    print(",".join(row))
       

    def Columnar(self):
        PipelineId = "levman"
        #Check for any patient metadata so we can augment output
        #The metadata file should have the format Patient,Visit,Attr1..AttrN
        Metadata = {} 
        if self.metadata and os.path.isfile(self.metadata):      
            with open(self.metadata, newline='') as f:
                reader = csv.reader(f)
                metaHeader = next(reader)
                for row in reader:   #iterate the metadata rows, add to dicitonary                    
                    for i in range(2,len(metaHeader)):    #iterate the cells of the row  
                        if row[0] not in Metadata:
                            Metadata[row[0]] = {}                        
                        if row[1] not in Metadata[row[0]]:
                            Metadata[row[0]][row[1]] = {}
                        
                        Metadata[row[0]][row[1]][metaHeader[i]]=row[i]
        #--------------------------HEADER-----------------------------------
        #Pring CSV Header using first patient measurement keys as columns.
        #If first patient isn't fully rendered, all keys will not appear
     
        header=[]
        header.append("PatientID")
        header.append("VisitId")
        #Add extra patient metadata if exists
        if self.metadata:
            for meta_i in range(2,len(metaHeader)):
                header.append(metaHeader[meta_i])  


        self.Segments = []#{}

        i=1
        segmentMap="%s/%s" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),"segmentMap.csv")
        with open(segmentMap) as fin:
            reader=csv.reader(fin, skipinitialspace=True, quotechar="'")
            p = re.compile('^ *#')   # if not commented          
            for row in reader:
                #print("%s,%s" %(i,row))
                if(i>1 and not p.match(row[0])): 
                    self.Segments.append({'roi':row[0],'roiname':row[1],'asymmetry':row[2]})
                i=i+1

        measurementKeys = []

        for s in self.Segments:
            segment=s['roi'].zfill(4)
            
            segmentName=s['roiname']                                            
            for c in self.Segments:
                counterpart=c['roi'].zfill(4)
                counterpartName=c['roiname']                               
                if (segment!=counterpart and segment<counterpart):                        
                    methods=[]  #Methods represents the possible ROI switches to trackvis, e.g methods = ["roi","roi_end"]
                    methodFile="%s/%s" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),"methods.txt")
                    with open(methodFile) as fin:
                        reader=csv.reader(fin, skipinitialspace=True, quotechar="'")
                        p = re.compile('^ *#')   # if not commented          
                        for row in reader:
                            if(not p.match(row[0])):                    
                                methods.append(row[0])                    
                    for method in methods:
                        #print("Rendering segment %s counterpart %s method %s" %(segment, counterpart, method))
                        if segment != counterpart:
                            #print("levman/%s-%s-%s-Tractlength" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-Tractlength" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-NumTracts" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-TractsToRender" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-LinesToRender" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-MeanTractLen" %(segment,counterpart,method))
                            measurementKeys.append(r"levman/%s-%s-%s-MeanTractLen_StdDev" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-VoxelSizeX" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-VoxelSizeY" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-VoxelSizeZ" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-meanFA" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-stddevFA" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-meanADC" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-stddevADC" %(segment,counterpart,method))

                            measurementKeys.append("levman/%s-%s-%s-Tractlength-asymidx" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-NumTracts-asymidx" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-TractsToRender-asymidx" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-LinesToRender-asymidx" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-MeanTractLen-asymidx" %(segment,counterpart,method))
                            measurementKeys.append(r"levman/%s-%s-%s-MeanTractLen_StdDev-asymidx" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-VoxelSizeX-asymidx" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-VoxelSizeY-asymidx" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-VoxelSizeZ-asymidx" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-meanFA-asymidx" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-stddevFA-asymidx" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-meanADC-asymidx" %(segment,counterpart,method))
                            measurementKeys.append("levman/%s-%s-%s-stddevADC-asymidx" %(segment,counterpart,method))
                            

        for k in measurementKeys:            
            header.append(k)
                               
        print(",".join(header))
                        
        #Print CSV Data ------------BODY------------------------------------
        for p in self.Patients:
            for v in p.Visits:            
                row=[]                
                row.append(p.PatientId)            
                row.append(v.VisitId)

                for meta_i in range(2,len(metaHeader)):
                    meta=metaHeader[meta_i]
                    if p.PatientId in Metadata and v.VisitId in Metadata[p.PatientId] and meta in Metadata[p.PatientId][v.VisitId] :
                        row.append(Metadata[p.PatientId][v.VisitId][meta])
                    else:
                        row.append("")                
                measurements = v.GetMeasurements()   
                        
                #=====================================================
                asymMeasuresToAdd = {}                
                for m in measurements:
                    if len(m)>8 and m[-8] != "-asymidx":
                        #print(m)
                        m0 = re.match("^"+PipelineId+"\/(\w+)-(\w+)-(\w+)-(\w+)",m)
                        
                        if m0:
                            l_roi = m0.group(1)
                            l_roiE = m0.group(2)
                            l_method = m0.group(3)
                            l_measure = m0.group(4)

                            l_roiC=""
                            l_roiEC=""

                            
                            for s in self.Segments:                        
                                if s['roi']==l_roi:                            
                                    l_roiC = s['asymmetry']
                                if s['roi']==l_roiE:
                                    l_roiEC = s['asymmetry']
                            #print("%s, %s, %s, %s" %(l_roi,l_roiE,l_roiC,l_roiEC))
                            asymCounterpart = PipelineId+"/%s-%s-%s-%s" %(l_roiC,l_roiEC,l_method,l_measure) 
                            #print(asymCounterpart)                   
                            if asymCounterpart in measurements:
                                if v.is_number(measurements[m]) and v.is_number(measurements[asymCounterpart]) and float(measurements[asymCounterpart]) != 0:
                                    asymIdx=float(measurements[m]) / float(measurements[asymCounterpart])                            
                                    asymMeasuresToAdd["%s-asymidx" %(m)] = asymIdx

                #print(asymMeasuresToAdd)
                #return
                for newm in asymMeasuresToAdd:
                    if v.is_number(str(asymMeasuresToAdd[newm])):
                        measurements[newm]=str(asymMeasuresToAdd[newm])


                #===================================

                #print(measurements)
                for k in measurementKeys:
                    #print(k)
                    if k in measurements:                              
                        row.append(measurements[k])
                    else:
                        #print("not found: patient id:%s measurement:%s" %(p.PatientId,k))
                        row.append("")                                      
                print(",".join(row))