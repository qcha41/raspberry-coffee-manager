# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import pandas as pd
from  threading import Lock
import sqlite3
    
      
def create(dbPath):

    dtb = Database(dbPath)
            
    dtb.write(''' CREATE TABLE Users (
            id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            tag         INT,
            email       TEXT,
            donation    REAL CHECK(donation>=0) NOT NULL,
            CONSTRAINT unique_name UNIQUE (name),
            CONSTRAINT unique_tag UNIQUE (tag),
            CONSTRAINT unique_email UNIQUE (email) )''')    
    
    dtb.write(''' CREATE TABLE UserOperations (
            id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT NOT NULL,
            user        INT NOT NULL,
            label       INT NOT NULL,
            value       REAL NOT NULL,
            FOREIGN KEY(user) REFERENCES Users(id)) ''')
    
    dtb.write(''' CREATE TABLE SystemOperations (
            id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT NOT NULL,
            label        TEXT NOT NULL,
            caps        INT NOT NULL,
            value       REAL NOT NULL) ''')
    
    dtb.close()
    
    
    
    
class Database():
    
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
        
        
        
def convert_old_version(oldDBpath,newDBpath):
    
    oldDtb = Database(oldDBpath)
    newDtb = Database(newDBpath)
    
    # Users
    users = oldDtb.read('SELECT * FROM Users')
    users.to_sql('Users',newDtb.dtb,if_exists='append',index=False)
    
    # User op
    d = {1:'Conso',2:'Donation',3:'Recharge'}
    userop = oldDtb.read('SELECT * FROM UserOperations')
    userop.rename(columns={'item':'label'},inplace=True)
    userop.loc[:,'label'] = userop.label.apply(lambda x: d[x])
    userop.to_sql('UserOperations',newDtb.dtb,if_exists='append',index=False)
    
    # System op
    donations = oldDtb.read('SELECT * FROM Donations')
    systemop = oldDtb.read('SELECT * FROM SystemOperations')
    systemop.rename(columns={'description':'label'},inplace=True)
    for i in range(len(donations)) :
        systemop = systemop.append({'timestamp':donations.iloc[i]['timestamp'],
                                    'label':'Donation',
                                    'caps':0,
                                    'value': -donations.iloc[i]['value']},ignore_index=True)
    systemop.to_sql('SystemOperations',newDtb.dtb,if_exists='append',index=False)
    
    oldDtb.close()
    newDtb.close()
    

