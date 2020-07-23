#from crushdb import repository
import crushdb
import sys
sample=sys.argv[1]
visit=1


repo=crushdb.repository()

for i in range(1,182):    
    for j in range(1,182):        
        repo.upsert(sample,visit,i,j,'roi','a',124)
        repo.upsert(sample,visit,i,j,'roi','b',124)
        repo.upsert(sample,visit,i,j,'roi','c',124)
        repo.upsert(sample,visit,i,j,'roi','d',124)
        repo.upsert(sample,visit,i,j,'roi','e',124)
        repo.upsert(sample,visit,i,j,'roi','f',124)
        repo.upsert(sample,visit,i,j,'roi','g',124)
        repo.upsert(sample,visit,i,j,'roi','h',124)

        repo.upsert(sample,visit,i,j,'roi_end','a',124)
        repo.upsert(sample,visit,i,j,'roi_end','b',124)
        repo.upsert(sample,visit,i,j,'roi_end','c',124)
        repo.upsert(sample,visit,i,j,'roi_end','d',124)
        repo.upsert(sample,visit,i,j,'roi_end','e',124)
        repo.upsert(sample,visit,i,j,'roi_end','f',124)
        repo.upsert(sample,visit,i,j,'roi_end','g',124)
        repo.upsert(sample,visit,i,j,'roi_end','h',124)
        

#x = repo.get(1,4,'c','d')

#print(f"measured vale:{x}")




