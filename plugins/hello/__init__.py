import time

def run(visit):
        
    print("\tHello from a plugin!  [%s] data points already detected" %(len(visit.data[visit.PatientId][visit.VisitId])))
    
    '''
    Do something amazing!
    '''
    visit.SetValue("hello",12345)
    visit.SetValue("RenderTime",int(time.time()))
    visit.Commit()

    measure = visit.GetValue("hello")
    
    
    pass
    