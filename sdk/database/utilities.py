#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 12:05:10 2018

@author: pi
"""
import sqlite3
import os
import pandas as pd
from threading import Lock

class RawDatabase():
    
    def __init__(self,dbPath) :
        
        self.dtb = sqlite3.connect(dbPath,check_same_thread=False)
        self.cursor = self.dtb.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")
        self.lock = Lock()
        self.logger = None
        
    # ----------------------------------------------------------------------
    # Read and write
    # -----------------------------------------------------------------------
        
    def write(self,command):
        self.lock.acquire()
        try : 
            self.cursor.execute(command)
            self.dtb.commit()
        except sqlite3.Error as e :
            if self.logger is not None :
                self.logger.log(command+' '+str(e))
        self.lock.release()
    
    def read(self,command):
        self.lock.acquire()
        try : 
            result = pd.read_sql(command,self.dtb)
        except sqlite3.Error as e :
            if self.logger is not None :
                self.logger.log(command+' '+str(e))
            result = None
        self.lock.release()
        return result

    
    def close(self):
        self.dtb.close()
        
    
if __name__ == '__main__':
    a = RawDatabase('database')
