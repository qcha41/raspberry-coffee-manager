# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import pandas as pd
from  threading import Lock
import sqlite3
import os    
    

class Database():
    
    def __init__(self,path) :
        
        path = os.path.realpath(path)
        if os.path.exists(path) is False : new = True
        else : new = False
        
        self.lock = Lock()
        self.logger = print
        self.auto_commit = True
        
        self.dtb = sqlite3.connect(path,check_same_thread=False)
        self.cursor = self.dtb.cursor()
        if new is True : self.initialize()   
        self.cursor.execute("PRAGMA foreign_keys = ON")
        self.dtb.commit()
        
        
    # ----------------------------------------------------------------------
    # Read and write
    # -----------------------------------------------------------------------
        
    def write(self,command):
        self.lock.acquire()
        try : 
            self.cursor.execute(command)
            if self.auto_commit is True : self.commit()
        except sqlite3.Error as e :
            if self.logger is not None :
                self.logger(command+' '+str(e))
        self.lock.release()
    
    def read(self,command):
        self.lock.acquire()
        try : 
            result = pd.read_sql(command,self.dtb)
        except sqlite3.Error as e :
            if self.logger is not None :
                self.logger(command+' '+str(e))
            result = None
        self.lock.release()
        return result

    def commit(self):
        self.dtb.commit()
        
    def close(self):
        self.dtb.close()
        
    def initialize(self):
        
        self.write(''' CREATE TABLE users (
                            id                      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            name                    TEXT NOT NULL,
                            tag                     INT,
                            email                   TEXT,
                            auto_donation           REAL CHECK(auto_donation>=0) NOT NULL,
                            active                  INT NOT NULL DEFAULT 1,
                            CONSTRAINT unique_tag   UNIQUE (tag),
                            CONSTRAINT unique_email UNIQUE (email) )''')    
    
        self.write(''' CREATE TABLE account_operations (
                            id                      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            timestamp               TEXT NOT NULL,
                            label                   TEXT NOT NULL,
                            user                    INT NOT NULL,
                            value                   REAL NOT NULL,
                            checked                 INT NOT NULL DEFAULT 0,
                            FOREIGN KEY(user)       REFERENCES users(id) ) ''')
    
        self.write(''' CREATE TABLE caps_operations (
                            id                      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            timestamp               TEXT NOT NULL,
                            label                   TEXT NOT NULL,
                            user                    INT,
                            qty                     INT NOT NULL,
                            value                   REAL NOT NULL,
                            FOREIGN KEY(user)       REFERENCES users(id) ) ''')
        
        self.write(''' CREATE TABLE donation_operations (
                            id                      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            timestamp               TEXT NOT NULL,
                            label                   TEXT NOT NULL,
                            user                    INT,
                            value                   REAL NOT NULL,
                            FOREIGN KEY(user)       REFERENCES users(id) ) ''')
            
    
        
       