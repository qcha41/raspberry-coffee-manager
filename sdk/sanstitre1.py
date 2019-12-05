# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 08:21:39 2019

@author: qchat
"""

class Administration :
    
    def __init__(self):
        
    def add_expense(self):
        
    def users_balance(self):
        
    def system_balance(self):
        
    def 


class UserManager :
    
    def __init__(self):
        
        self._users = {}
        
        # Load
        for name in self.list_users() :
            self._users[name] = User(name)
        
    def create_user(self,name):
        
        ''' Create a new user '''
        
        default_donation = config('newUserDefaultDonation')
        database.write("INSERT INTO Users (name,donation) VALUES ('%s',%g)"%(name,default_donation)) 
        self._users[name] = User(name)

    def get_user(self,name):
        
        ''' Returns the user with corresponding name '''
        
        return self._users[name]
        
    def get_user_by_tag(self,tag):
        
        ''' Returns the user with corresponding tag '''
        
        ans = database.read("SELECT name FROM Users WHERE tag=%i"%tag)['name'][0]
        
    def list_users(self):
        
        ''' Returns the list of users '''
        
        tuple(self.read("SELECT name FROM Users")['name'])
        

    

class User :
    
    def __init__(self,manager,name) :
        
        self.manager = manager
        self.name = name
        self.id = database.read("SELECT id FROM Users WHERE name=%i"%name)['id'][0]
        
    
    def balance(self):
        
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
        
    def add_payment(self,value):
        
        ''' Add a new payment '''
        
        