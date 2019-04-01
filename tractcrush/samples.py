import os, sys,inspect,re
#from pathlib import Path
from tractcrush.patient import Patient
import csv
import math

class Samples:
    Count=0
    
    
    def __init__(self,rootDir,force,voi,recrush,metadata,fixmissing):
        self.Patients=[]
        self.force=force
        self.voi=voi
        self.recrush=recrush
        self.metadata=metadata
        self.fixmissing=fixmissing
        self.rootDir=rootDir

        dirs = os.listdir( rootDir )
        
        for file in dirs:
           
            patient_dir = "%s/%s" % (rootDir,file)
            if os.path.isdir(patient_dir):
                visits = os.listdir(patient_dir)
                for v in visits:
                    if(not os.path.islink("%s/%s" %(patient_dir,v))):
                        mri_dir = "%s/%s/Freesurfer/mri" % (patient_dir,v)
                        if os.path.exists(mri_dir):
                            #print "%s/%s/mri" %(patient_dir,v)
                            #visit_dir = "%s/%s/01" % (rootDir,file)
                            #if os.path.exists(visit_dir): #assume if at least one visit then patient
                            self.Count+=1
                            patient=Patient(patient_dir,self.force,self.voi,self.recrush,self.fixmissing)
                            self.Patients.append(patient)
                                   
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

                        

                    #row.append(measurements[m])                    
                    print(",".join(row))
                #print("---"+str(measurements))


                # for m in measurements:                  
                #     row=[]                
                #     row.append(p.PatientId)            
                #     row.append(v.VisitId)

                #     for meta_i in range(2,len(metaHeader)):
                #         meta=metaHeader[meta_i]
                #         if p.PatientId in Metadata and v.VisitId in Metadata[p.PatientId] and meta in Metadata[p.PatientId][v.VisitId] :
                #             row.append(Metadata[p.PatientId][v.VisitId][meta])
                #         else:
                #             row.append("")

                #     #What do we know about this ROI?
                #     m0 = re.match("^(\w+)-(\w+)-(\w+)-(\w+)",m)
                #     if m0 and m0.group(1) in Features:                         
                #         roi=Features[m0.group(1)]['ROI']
                #         roiLabel=Features[m0.group(1)]['ROI Label']
                #         asymIdx=Features[m0.group(1)]['Asymmetry Counterpart']
                #         lw=Features[m0.group(1)]['Left or Right']
                #         wg=Features[m0.group(1)]['White or Grey']                       
                #         cn=Features[m0.group(1)]['Common Name']
                #         method=m0.group(3)
                #         measure=m0.group(4)
                #     else:
                #         roi=m0.group(1)
                #         roiLabel=""
                #         asymIdx=""
                #         lw=""
                #         wg=""
                #         cn=""
                #         method=m0.group(3)
                #         measure=m0.group(4)

                #     row.append(roi)
                #     row.append(roiLabel)
                #     row.append(asymIdx)
                #     row.append(lw)
                #     row.append(wg)
                #     row.append(cn)
                #     row.append(method)
                #     row.append(measure)

                #     row.append(m)
                #     row.append(measurements[m])
                #     print(",".join(row))
            

    def Columnar(self):


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
                

        for p in self.Patients:            
            for v in p.Visits:                                
                measurements = v.GetMeasurements()

                measurementKeys = sorted(measurements.keys())
                for k in measurementKeys:
                    header.append(k)
                break
            break
        break
                        
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
                for k in measurementKeys:
                    if measurements[k]:
                        row.append(measurements[k])
                    else   
                        row.append("")
                    
                  
                print(",".join(row))