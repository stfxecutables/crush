#!/usr/bin/env python3

import os
import psycopg2 as pg

from decimal import Decimal
from functools import wraps
from psycopg2.pool import ThreadedConnectionPool

from contextlib import contextmanager


class repository:
    
    def __init__(self):   
        self.pool = self.connect()

        schema=os.path.join(os.path.dirname(__file__), 'schema.sql')             

        conn = self.pool.getconn()
        self.createdb(conn,schema)
        self.pool.putconn(conn)

    def connect(self,env="CRUSH_DATABASE_URL", connections=2):
        """
        Connect to the database using an environment variable CRUSH_DATABASE_URL.
        """
        url = os.getenv(env)
        if not url:
            raise ValueError("no database url specified.  CRUSH_DATABASE_URL environment variable must be set using example:\npostgresql://user@localhost:5432/dbname")

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
        except Exception as e:
            conn.rollback()
            raise e
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
            conn.rollback()           
        finally:
            conn.reset()
            self.pool.putconn(conn)
            
            
    def update_measurement(self,conn,roi_start,roi_end,method,measurement,measured):
        """
        Create or insert the measured value in measurements table
        """  
        measured = Decimal(measured)
        with conn.cursor() as curs:
            sql="""INSERT INTO measurements (roi_start,roi_end,method,measurement,measured)
                    VALUES('%s','%s','%s','%s','%d') 
                    ON CONFLICT (roi_start,roi_end,method,measurement) 
                    DO 
                        UPDATE SET measured = EXCLUDED.measured""" %(roi_start,roi_end,method,measurement,measured)            
            curs.execute(sql)

            
    def get_measurement(self,conn,roi_start,roi_end,method,measurement):
        """
        fetch the measured value in measurements table
        """
        with conn.cursor() as curs:
            sql=(
                    """select measured from measurements where roi_start=%s and roi_end=%s
                    and method=%s and measurement=%s
                    """
             )               
            curs.execute(sql,(roi_start,roi_end,method,measurement))   
            row = curs.fetchone()             
            measured = row[0]                    
        
        measured = Decimal(measured)        
        return measured


    @transact
    def upsert(self,conn, roi_start,roi_end,method,measurement,measured):
        self.update_measurement(conn,roi_start,roi_end,method,measurement,measured)

    @transact
    def get(self,conn, roi_start,roi_end,method,measurement):        
        x=self.get_measurement(conn,roi_start,roi_end,method,measurement)                
        return x


