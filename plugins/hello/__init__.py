import time

pipelineId="hello"

def run(visit):
        
    print("\tHello!  [%s] data points already detected" %(len(visit.data[visit.PatientId][visit.VisitId])))
    
    '''
    Do something amazing!
    '''
    visit.SetValue(pipelineId,"x1",12345)
    visit.SetValue(pipelineId,"x2",67890)
    visit.SetValue(pipelineId,"RenderTime",int(time.time()))
    visit.Commit()

    measure = visit.GetValue(pipelineId,"RenderTime")
    print(measure)
    
    
    pass
    
def csv(Patients,**kwargs):

    measureNames = ['x1','x2'] 


    if ('metadata' in kwargs):
        Metadata = kwargs['metadata']
        headerNames = Metadata['Header']

    #Print CSV Header
    row=[]
    row.append("PatientId")
    row.append("VisitId")
    if ('metadata' in kwargs):
        for meta_i in range(2,len(headerNames)):
            meta=headerNames[meta_i]
            row.append(meta)  

    for mn in measureNames:            
        row.append(mn)
  
    print(",".join(row))

    #Print CSV Data
    for p in Patients:
        for v in p.Visits:
            measurements = v.GetMeasurements()   

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
            
            for mn in measureNames:
                try:
                    row.append(v.GetValue(pipelineId,mn))
                except:
                    row.append("!")

            print(",".join(row))

