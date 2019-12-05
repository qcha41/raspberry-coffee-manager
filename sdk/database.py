# -*- coding: utf-8 -*-
"""
Éditeur de Spyderc QUENTIN CHATEILLER

Ceci est un script temporaire.
"""
from __future__ import division

import os
import sqlite3
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

class Database(RawDatabase):
    
    def __init__(self,sdk) :
        self.sdk = sdk
        
        RawDatabase.__init__(self,os.path.join(sdk.dataFolderPath,'database.db'))
        self.logger = sdk.logger
        

    
    # -------------------------------------------------------------------------
    # Users Table
    # -------------------------------------------------------------------------
    
    # New entry
    
    def newUser(self,name):
        defaultDonation = self.sdk.var.getValue('newUserDefaultDonation')
        self.write("INSERT INTO Users (name,donation) VALUES ('%s',%g)"%(name,defaultDonation))

    def getUserDict(self):
        data = self.read("SELECT id,name FROM Users")
        data.set_index('id', inplace=True)
        return data.to_dict()['name']
    
    
    
    
    # General info
    
    def getUserInfoList(self,infoType):
        return tuple(self.read("SELECT %s FROM Users WHERE %s IS NOT NULL"%(infoType,infoType))[infoType])
    
    def getUserTagList(self):
        return self.getUserInfoList('tag')
    
    def getUserList(self):
        return self.getUserInfoList('id')
        
    def getUserNameList(self):
        return self.getUserInfoList('name')
    
    def getUserEmailList(self):
        return self.getUserInfoList('email')
        
    def getUsersNb(self):
        return self.read("SELECT count(id) FROM Users")['count(id)'][0] 
    
    
    
    # Get user info
    
    def getUserInfo(self,ID,infoType):
        assert infoType in ['name','tag','email','donation']
        ans = self.read("SELECT %s FROM Users WHERE id=%i"%(infoType,ID))[infoType]
        if len(ans) == 1 :
            return ans[0]
        else:
            return None
    
    def getUserName(self,ID):
        return self.getUserInfo(ID,'name')
    
    def getUserTag(self,ID):
        return self.getUserInfo(ID,'tag')
    
    def getUserEmail(self,ID):
        return self.getUserInfo(ID,'email')
    
    def getUserDonation(self,ID):
        return self.getUserInfo(ID,'donation')
    
    
    
    
    # Get user by info
    
    def getUserByInfo(self,infoType,value):
        assert infoType in ['tag','name']
        if type(value) == str :
            ans = self.read("SELECT id FROM Users WHERE %s='%s'"%(infoType,value))['id']
        elif type(value) == int :
            ans = self.read("SELECT id FROM Users WHERE %s=%i"%(infoType,value))['id']
        if len(ans) == 1 :
            return ans[0]
        else:
            return None
    
    def getUserByTag(self,tag):
        return self.getUserByInfo('tag',tag)
    
    def getUserByName(self,name):
        return self.getUserByInfo('name',name)



    # Set user info
        
    def setUserInfo(self,ID,infoType,value):
        if type(value) == str :
            self.write("UPDATE Users SET %s = '%s' WHERE id = %i"%(infoType,value,ID))
        elif type(value) == int :
            self.write("UPDATE Users SET %s = %i WHERE id = %i"%(infoType,value,ID))
        elif value is None :
            self.write("UPDATE Users SET %s = NULL WHERE id = %i"%(infoType,ID))
        elif type(float(value)) == float :
            self.write("UPDATE Users SET %s = %.2f WHERE id = %i"%(infoType,value,ID))
            
    def setUserName(self,ID,name):
        self.setUserInfo(ID,'name',name)

    def setUserTag(self,ID,tag):
        self.setUserInfo(ID,'tag',tag)
    
    def setUserEmail(self,ID,email):
        self.setUserInfo(ID,'email',email)
        
    def setUserDonation(self,ID,donation):
        self.setUserInfo(ID,'donation',donation)
    
    
    
    # -------------------------------------------------------------------------
    # Items Table
    # -------------------------------------------------------------------------
    
    def getItemByName(self,name):
        return self.read("SELECT id FROM Items WHERE name='%s'"%name)['id'][0]
        
    def getItemDict(self):
        data = self.read("SELECT * FROM Items")
        data.set_index('id', inplace=True)
        return data.to_dict()['name']

    # -------------------------------------------------------------------------
    # User Operations Table
    # -------------------------------------------------------------------------

    # New operation
    
    def newUserOperation(self,user,item,value):
        timestamp = self.sdk.system.getTimeStamp()
        self.write('''INSERT INTO UserOperations
                     (timestamp,user,item,value)
                     VALUES ('%s',%i,%i,%.2f)'''%(timestamp,user,item,value))
  

    
    # Get general operation info
    
    def getUserOperationLast(self):
        return self.read("SELECT max(id) FROM UserOperations")['max(id)'][0]
    
    def getUserOperationsNb(self):
        return self.read("SELECT count(id) FROM UserOperations")['count(id)'][0]   
    
    def getUserOperationsNbByItem(self,ID):
        result = self.read("SELECT count(id) FROM UserOperations WHERE item=%i"%ID)['count(id)'][0]
        if result is None :
            result = 0
        return result
    
    def getUserOperationsValueByItem(self,ID):
        result = self.read("SELECT sum(value) FROM UserOperations WHERE item=%i"%ID)['sum(value)'][0]
        if result is None :
            result = 0
        return result
        
    def getUserOperationsValueByItemByUser(self,item,user):
        result = self.read("SELECT sum(value) FROM UserOperations WHERE item=%i AND user=%i"%(item,user))['sum(value)'][0]
        if result is None :
            result = 0
        return result
    
    def getUserOperationsByDate(self,timestamp):
        return self.read("""SELECT * FROM UserOperations 
                            WHERE date(timestamp)=date('%s')"""%(timestamp))
    
    def getUserOperationsByUserByDate(self,user,timestamp):
        return self.read("""SELECT * FROM UserOperations 
                            WHERE date(timestamp)=date('%s')
                            AND user=%i"""%(timestamp,user))
    
    def getNbCapsToday(self,user):
        today = self.sdk.system.getTimeStamp()
        caps = self.getItemByName('Caps')
        result = self.getUserOperationsByUserByDate(user,today)
        return len(result[result['item']==caps])

        
    # Get operation info
    
    def getUserOperationContent(self,ID):
        return self.read("SELECT * FROM UserOperations WHERE id=%i"%ID)
    
    def getUserOperationInfo(self,ID,infoType):
        ans = self.read("SELECT %s FROM UserOperations WHERE id=%i"%(infoType,ID))[infoType]
        if len(ans) == 1 :
            return ans[0]
        else:
            return None
        
    def getUserOperationItem(self,ID):
        return self.getUserOperationInfo(ID,'item')
        
    def getUserOperationUser(self,ID):
        return self.getUserOperationInfo(ID,'user')
        
    def getUserOperationValue(self,ID):
        return self.getUserOperationInfo(ID,'value')
        
    
    # -------------------------------------------------------------------------
    # Donation Table
    # -------------------------------------------------------------------------
        
    def newDonation(self,value):
        timestamp = self.sdk.system.getTimeStamp()
        self.write('''INSERT INTO Donations
                     (timestamp,value)
                     VALUES ('%s',%.2f)'''%(timestamp,value))
        
    def getDonationsValue(self):
        result = self.read("SELECT sum(value) FROM Donations")['sum(value)'][0]
        if result is None :
            return 0
        else :
            return result
    
    def getDonationList(self):
        return tuple(self.read("SELECT id FROM Donations"))
    
    def getDonationContent(self,ID):
        return self.read("SELECT * FROM Donations WHERE id=%i"%ID)
    
    def getDonations(self):
        return self.read("SELECT * FROM Donations")

    
    
    # -------------------------------------------------------------------------
    # System Operation Table
    # -------------------------------------------------------------------------
        
    # New expense
    
    def newSystemOperation(self,description,caps,value):
        timestamp = self.sdk.system.getTimeStamp()
        self.write('''INSERT INTO SystemOperations
                     (timestamp,description,caps,value)
                     VALUES ('%s','%s' ,%i,%.2f)'''%(timestamp,description,caps,value))
        
        
    # Get general expense info
    
    def getSystemOperationLast(self):
        return self.read("SELECT max(id) FROM SystemOperations")['max(id)'][0]
    
    def getSystemOperationInfo(self,ID,infoType):
        ans = self.read("SELECT %s FROM SystemOperations WHERE id=%i"%(infoType,ID))[infoType]
        if len(ans) == 1 :
            return ans[0]
        else:
            return None
    
    def getSystemOperationCaps(self,ID):
        return self.getSystemOperationInfo(ID,'caps')
    
    def getSystemOperationValue(self,ID):
        return self.getSystemOperationInfo(ID,'value')
    
    def getSystemOperationsCaps(self):
        result = self.read("SELECT sum(caps) FROM SystemOperations")['sum(caps)'][0]
        if result is None :
            result = 0
        return result
    
    def getSystemOperationsValue(self):
        result = self.read("SELECT sum(value) FROM SystemOperations")['sum(value)'][0]
        if result is None :
            result = 0
        return result
    
    
    def getSystemOperations(self):
        return self.read("SELECT * FROM SystemOperations")
                
    
    # -------------------------------------------------------------------------
    # High level functions
    # -------------------------------------------------------------------------
    def getNbCapsUsed(self):
        item = self.getItemByName('Caps')
        return self.getUserOperationsNbByItem(item)
    
    def getValueCapsUsed(self):
        item = self.getItemByName('Caps')
        return - self.getUserOperationsValueByItem(item)
    
    def getUsersRechargeNb(self):
        item = self.getItemByName('Recharge')
        return self.getUserOperationsNbByItem(item)
    
    def getUsersRechargeValue(self):
        item = self.getItemByName('Recharge')
        return self.getUserOperationsValueByItem(item)
    
    def getUsersDonationNb(self):
        item = self.getItemByName('Donation')
        return self.getUserOperationsNbByItem(item)
    
    def getUsersDonationValue(self):
        item = self.getItemByName('Donation')
        return - self.getUserOperationsValueByItem(item)
    
    def getUserBalance(self,user):
        result = self.read("SELECT sum(value) FROM UserOperations WHERE user=%i"%user)['sum(value)'][0]
        if result is None :
            result = 0
        return result
        
    def getUserTotalDonation(self,user):
        item = self.getItemByName('Donation')
        return - self.getUserOperationsValueByItemByUser(item,user)
    
    
    def getRemainingCaps(self):
        nbCapsSystem = self.getSystemOperationsCaps()
        nbCapsUsed = self.getNbCapsUsed()
        return nbCapsSystem - nbCapsUsed
    
    def getRemainingValue(self):
        expensesValue = -self.getSystemOperationsValue()
        consosValue = self.getValueCapsUsed()
        return expensesValue - consosValue
        
    def getCurrentCapsValue(self):
        caps = self.getRemainingCaps()
        if caps >0 :
            value = self.getRemainingValue()
            return round(value/caps,2)
        else :
            return 0.35
    
    
    def getUserAdvance(self):
        result = self.read("SELECT sum(value) FROM UserOperations")['sum(value)'][0]
        if result is None :
            result = 0
        return result

        
    
    
    
    
    def getDonationToProcess(self):
        user = - self.getUsersDonationValue()
        system = self.getDonationsValue()
        return user - system
    
    
    def getSystemBalance(self):
        expenses = - self.getSystemOperationsValue()
        userRecharges = self.getRechargesValue()
        donations = - self.getDonationsValue()
        return userRecharges - donations - expenses

    # -------------------------------------------------------------------------
    # Other
    # -------------------------------------------------------------------------
    
    
        
    def isTagAdmin(self,tag):
        return tag == 25089510172
    
    


        
if __name__ == '__main__' :
    db = Database()
    
