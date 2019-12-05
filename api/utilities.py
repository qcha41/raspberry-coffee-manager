# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 08:21:39 2019

@author: qchat
"""
from database import Database

class System :
    
    def __init__(self):
        
        self.dtb = database.Database()
        
    # Users
    
    def add_user(self,name):
        assert name not in self.list_users()
        default_donation = config('default_donation')
        self.dtb.write("INSERT INTO Users (name,donation) VALUES ('%s',%g)"%(name,default_donation)) 
        
    def get_user(name):
        assert name in self.list_users()
        return User(self.dtb,name)

    # Operations
        
    def add_donation(self,cost):
        
    def add_caps_purchase(self,nb_caps,cost):
        
    def add_supply_purchase(self,value):
        
    def get_donation_to_do(self):
        
    def get_balance(self):       
        
    # Caps stock
        
    def update_caps_stock(self,nb_caps):
        
    def get_caps_stock(self):
        
    def list_users(self):
        return tuple(self.read("SELECT name FROM Users").name)
    
    def list_tags(self):
        return tuple(self.read("SELECT tag FROM Users").tag)




class User :
    
    def __init__(self,system,name) :
        
        self.system = system
        self.dtb = system.dtb
        self.name = name
    
    def get_balance(self):
        
        ''' Returns the current account balance '''
        
        result = database.read("SELECT sum(value) FROM UserOperations WHERE user=%i"%user)['sum(value)'][0]
        if result is None : result = 0
        return result
    
        
    def rename(self,name):
        
        ''' Rename user '''
        
        assert name not in self.manager.list_users()
        database.write("UPDATE Users SET name = '%s' WHERE id = %i"%(value,self.id))
        self.name = name
        
    def set_email(self,email):
        
        ''' Set user email '''
        
        database.write("UPDATE Users SET email = '%s' WHERE id = %i"%(email,self.id))
        
    def get_email(self):
        
        ''' Returns current email '''
        return database.read("SELECT email FROM Users WHERE id = %i"%(self.id))['email'][0]
        
    def set_auto_donation(self,value):

        ''' Set the value of the auto donation '''
        
    def get_auto_donation(self):
        
        ''' Returns the value of the auto donation '''
        
    def set_tag(self,value):
        
        ''' Set the RFID tag of the user '''
        
    def get_tag(self):
        
        ''' Returns the RFID tag of the user '''
        
        
        
    def add_conso(self):
        
        ''' Add a new conso '''

    def add_donation(self):
        
        ''' Add a new donation '''
        
    def add_recharge(self,value):
        
        ''' Add a new recharge '''
        
        