#from crushdb import repository
import crushdb
import sys
import logging

sample=sys.argv[1]
visit=1

logger = logging.getLogger()
fhandler = logging.FileHandler(filename=f'crushdbtest.{sample}.log', mode='a')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)
logger.setLevel(logging.DEBUG)

logger.info(f'Test Initiated for sample {sample}') 

try :
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
except Exception as e:
    print(e)
    logger.error(f'Test failed ERROR:{e}')

logger.info(f'Test Completed for sample {sample}') 





