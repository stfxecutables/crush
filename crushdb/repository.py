#!/usr/bin/env python3

import os
import psycopg2 as pg
import logging
from decimal import Decimal
from functools import wraps
from psycopg2.pool import ThreadedConnectionPool

from contextlib import contextmanager

# Keep a text file to capture any errors.  
# I'm particularly interested in pooled connection failures 
# if there are too many concurrent connections.

logging.basicConfig(level=logging.INFO, 
    format='%(asctime)s %(message)s',
    filename='crushdb-repository.log')

class repository:
    
    def __init__(self):  
        # Establish a connection pool
        # Opening connections every time is expensive, lets open a few of them, 
        # and reuse them as neeed
        # The connections in the pool will be closed then the repository memory 
        # instance is destroyed
                   
        # default is to open a connection pool of at least 2 connections. 
        # see below minconn and maxconn 
        # Adjustments may be needed.

        self.pool = self.connect() 
                              
        logging.info('Repository Instantiated')

        #if the schema doesn't exist, create it using module code schema.sql       
        schema=os.path.join(os.path.dirname(__file__), 'schema.sql')    

        # want as little possible in next 3 lines,  between getconn and putconn              
        conn = self.pool.getconn()         
        self.createdb(conn,schema)          
        self.pool.putconn(conn)   
        # quick release of connection for anyone else waiting for a connection
        # from the pool 

    def __del__(self): 
        #Indicator in logs for when teardown happens, conns close      
        logging.info('Repository Uninstantiated') 

    def connect(self,env="CRUSH_DATABASE_URL", connections=2):
        """
        Connect to the database using an environment variable CRUSH_DATABASE_URL.
        """
        
        url = os.getenv(env)
        if not url:
            msg = '''no database url specified.  CRUSH_DATABASE_URL environment 
            variable must be set using example:
            postgresql://user@localhost:5432/dbname'''
            logging.error(msg)
            raise ValueError(msg)
        
        # Keep an open pool of 2 connections, but grow up to 4 as needed
        # The ThreadedConnectionPool will decide when to do garbage collection
        minconns = connections
        maxconns = connections * 2
        return ThreadedConnectionPool(minconns, maxconns, url)


    def createdb(self,conn, schema="schema.sql"):
        """
        Execute CREATE TABLE statements in the schema.sql file.
        """
        with open(schema, 'r') as f:
            sql = f.read()

        try:
            with conn.cursor() as curs:
                curs.execute(sql)
                conn.commit()
                logging.info('Repository Instantiated')
        except Exception as e:
            conn.rollback()
            logging.error(f'Failed to create schema, ERROR:{e}')
            raise e
    
    # This will be a decorator function used below for "upsert" and "get"
    # functions.
    def transact(func):
        """
        Creates a connection per-transaction, committing when complete or
        rolling back if there is an exception. It also ensures that the conn is
        closed when we're done.
        """

        @wraps(func)
        def inner(self,*args, **kwargs):            
            with self.transaction(name=func.__name__) as conn:                    
                ret=func(self,conn, *args, **kwargs)
                return ret    
        return inner
        
    @contextmanager
    def transaction(self,name="transaction", **kwargs):
        # This is the secret ingredient, allowing us to allocate and release 
        # resources (db connections) precisely when we want to.  This minimizes
        # the time we have the connection in use

        # Get the session parameters from the kwargs
        options = {
            "isolation_level": kwargs.get("isolation_level", None),
            "readonly": kwargs.get("readonly", None),
            "deferrable": kwargs.get("deferrable", None),
        }
        
        try:
            conn = self.pool.getconn()
            conn.set_session(**options)
            yield conn
            conn.commit()
        except Exception as e:
            print(e)
            logging.info(f'Transaction failed ERROR:{e}')
            conn.rollback()           
        finally:
            conn.reset()
            self.pool.putconn(conn)
            
            
    def update_measurement(self,conn,sample,visit,roi_start,roi_end,method,measurement,measured):
        """
        Create or insert the measured value in measurements table
        """  
        measured = Decimal(measured)
        try:
            with conn.cursor() as curs:
                sql="""INSERT INTO measurements (sample,visit,roi_start,roi_end,method,measurement,measured)
                    VALUES('%s','%s','%s','%s','%s','%s','%d') 
                    ON CONFLICT (sample,visit,roi_start,roi_end,method,measurement) 
                    DO 
                        UPDATE SET measured = EXCLUDED.measured""" %(sample,visit,roi_start,roi_end,method,measurement,measured)            
                curs.execute(sql)
        except Exception as e:
           logging.error(f"ERROR:{e} SQL:{sql}\n")
           raise e
            
    def get_measurement(self,conn,sample,visit,roi_start,roi_end,method,measurement):
        """
        fetch the measured value in measurements table
        """
        with conn.cursor() as curs:
            sql=(
                    """select measured from measurements where sample=%s and visit=%s and roi_start=%s and roi_end=%s
                    and method=%s and measurement=%s
                    """
             )               
            curs.execute(sql,(sample,visit,roi_start,roi_end,method,measurement))   
            row = curs.fetchone()             
            measured = row[0]                    
        
        measured = Decimal(measured)        
        return measured


    @transact
    def upsert(self,conn,sample,visit, roi_start,roi_end,method,measurement,measured):        
        self.update_measurement(conn,sample,visit,roi_start,roi_end,method,measurement,measured)

    @transact
    def get(self,conn,sample,visit, roi_start,roi_end,method,measurement):        
        x=self.get_measurement(conn,sample,visit,roi_start,roi_end,method,measurement)                
        return x


