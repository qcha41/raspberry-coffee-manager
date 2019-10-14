# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

from utilities import RawDatabase 
import datetime as dt
import pandas as pd
    
      
def create(dbPath):

    dtb = RawDatabase(dbPath)
            
    dtb.write(''' CREATE TABLE Users (
            id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            tag         INT,
            email       TEXT,
            donation    REAL CHECK(donation>=0) NOT NULL,
            CONSTRAINT unique_name UNIQUE (name),
            CONSTRAINT unique_tag UNIQUE (tag),
            CONSTRAINT unique_email UNIQUE (email) )''')
    
    dtb.write(''' CREATE TABLE Items (
            id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            CONSTRAINT unique_name UNIQUE (name) )''')
    
    dtb.write(''' INSERT INTO Items (name) VALUES ("Caps") ''')
    dtb.write(''' INSERT INTO Items (name) VALUES ("Donation") ''')
    dtb.write(''' INSERT INTO Items (name) VALUES ("Recharge") ''')
    
    
    dtb.write(''' CREATE TABLE UserOperations (
            id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT NOT NULL,
            user        INT NOT NULL,
            item        INT NOT NULL,
            value       REAL NOT NULL,
            FOREIGN KEY(user) REFERENCES Users(id),
            FOREIGN KEY(item) REFERENCES Items(id)) ''')
    
    dtb.write(''' CREATE TABLE SystemOperations (
            id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT NOT NULL,
            description TEXT NOT NULL,
            caps        INT NOT NULL,
            value       REAL NOT NULL) ''')
    
    dtb.write(''' CREATE TABLE Donations (
            id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT NOT NULL,
            value       REAL NOT NULL)''')
    
def importFromV2(oldDBpath,newDBpath):
    
    
    oldDtb = RawDatabase(oldDBpath)
    newDtb = RawDatabase(newDBpath)
    
    # Users
    users = oldDtb.read('SELECT * FROM Users')
    users.sort_values('id',inplace=True)
    users.rename(columns={'username':'name'},inplace=True)
    users['donation'] = 0.05
    users.to_sql('Users',newDtb.dtb,if_exists='append',index=False)
        
    # User operations backup
    d = {'Conso':1,'Recharge':3}
    userOpList = oldDtb.read('SELECT userid,date,time,label,value FROM Operations')
    userOpList['timestamp'] = userOpList['date']+','+userOpList['time']
    userOpList['timestamp'] = userOpList['timestamp'].apply(lambda x: dt.datetime.strptime(x,'%d-%m-%Y,%H:%M:%S').isoformat())
    userOpList.rename(columns={'userid':'user'},inplace=True)
    userOpList['item'] = userOpList['label'].apply(lambda x: d[x])
    userOpList.drop(columns=['date', 'time','label'],inplace=True)
    userOpList.to_sql('UserOperations',newDtb.dtb,if_exists='append',index=False)
        
    # System operation backup
    nbConso = len(userOpList.query('item == 1'))
    value = userOpList.query('item == 1')['value'].sum()
    expense = pd.DataFrame({'timestamp':['2017-08-29T08:55:35'],
               'description':['Backup conso V2'],
               'caps':[nbConso],
               'value':[float(value)]})
    expense.to_sql('SystemOperations',newDtb.dtb,if_exists='append',index=False)
    
    
    
#
#def importFromV1(oldDBname,newDBname):
#    
#    oldDtb = RawDatabase('/home/pi/')
#    newDtb = RawDatabase('/home/pi/coffee_manager/data/')
#    
#    # Users
#    users = oldDtb.read('SELECT id,user_name FROM Users')
#    users.sort_values('id',inplace=True)
#    users.rename(columns={'user_name':'username'},inplace=True)
#    for i in range(len(users)):
#        users.loc[i,'username'] = str(users['username'][i])[0] + str(users['username'][i][1:]).lower()
#    users.to_sql('Users',newDtb.dtb,if_exists='append',index=False)
#    
#    # Tags
#    tags = oldDtb.read('SELECT * FROM Tags')
#    for ID in tags['user_id'] :
#        tag = int(tags.query('user_id==%i'%ID)['rfid_id'])
#        newDtb.write('UPDATE Users SET tag = %i WHERE id = %i'%(tag,ID))
#
#    # Operations
#    op = oldDtb.read('SELECT * FROM Operations')
#    op.rename(columns={'user_id':'userid'},inplace=True)
#    op.loc[:,'label'] = op['label'].replace('conso','Conso')
#    op.loc[:,'label'] = op['label'].replace('payment','Recharge')
#    for i in range(len(op)):
#        print(i)
#        op.loc[i,'date'] = dt.strptime(op['date'][i], '%Y-%m-%d').strftime('%d-%m-%Y')
#    op.to_sql('Operations',newDtb.dtb,if_exists='append',index=False)
#    
#    # Caps
#    caps = oldDtb.read('SELECT * FROM Caps')
#    for i in range(len(caps)):
#        print(i)
#        caps.loc[i,'date'] = dt.strptime(caps['date'][i], '%Y-%m-%d').strftime('%d-%m-%Y')
#    caps.to_sql('Caps',newDtb.dtb,if_exists='append',index=False)
#    
#
#import os
#try :
#    os.remove(os.path.realpath('../../data/new.db'))
#except :
#    pass
#create('/home/pi/coffee_manager/data')
#importFromV1('database_ref','new')