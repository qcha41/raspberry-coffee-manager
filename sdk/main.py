#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 11:13:09 2018

@author: pi
"""

import sys
print(sys.version)

from .sensors.main import Sensors
from .images.main import Images
from .email.main import Email
from .database.main import Database
from .controllers.main import Controllers
from .logger.main import Logger
from .variables.main import Variables
from .system.main import System

import os



class SDK():
    
    def __init__(self):
      
        self.dataFolderPath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),'data')
        self.system = System(self)      
        self.var = Variables()
        self.logger = Logger(self)
        self.sensors = Sensors(self)
        self.database = Database(self)
        self.email = Email(self)
        self.controllers = Controllers(self)
        self.images = Images(self)
        
        self.updateCapsPrice()

        
    def stopThreads(self):
        self.controllers.stopThreads()
        self.sensors.stopThreads()
    
    # -------------------------------------------------------------------------
    # Conso
    # -------------------------------------------------------------------------
    
    def addConso(self,user):
        
        assert user in self.database.getUserList()
        
        # Donation
        donation = self.database.getItemByName('Donation')
        donationValue = - self.database.getUserDonation(user)
        if donationValue != 0 :
            self.database.newUserOperation(user,donation,donationValue)
        
        # Caps
        caps = self.database.getItemByName('Caps')
        capsValue = - self.var.getValue('capsPrice')
        self.database.newUserOperation(user,caps,capsValue)
        
        # Beep
        self.controllers.buzzer.beep()
                          
        # Update caps price
        self.updateCapsPrice()
                                 
        # Balance - mail             
        userBalance = self.database.getUserBalance(user)
        if userBalance < 0 :
            if self.var.getValue('email') is True :
                email = self.database.getUserEmail(user)
                name = self.database.getUserName(user)
                self.email.negativeBalance(email,name,userBalance)
        elif userBalance<10 and (userBalance-donationValue-capsValue)>10:
            if self.var.getValue('email') is True :
                email = self.database.getUserEmail(user)
                name = self.database.getUserName(user)
                self.email.lowBalance(email,name)            
            
        
    def checkBalance(self,user):

        userBalance = self.database.getUserBalance(user)
        
        
            
            
            
        
        
    def addRecharge(self,user,value):
        prevBalance = self.database.getUserBalance(user)
        
        item = self.database.getItemByName('Recharge')
        self.database.newUserOperation(user,item,value)
        
        newBalance = self.database.getUserBalance(user)
        username = self.database.getUserName(user)
        
        self.email.notifyRecharge(username,value,prevBalance,newBalance)
        
    def newExpense(self,description,caps,value):
        self.database.newSystemOperation(description,caps,value)
        self.updateCapsPrice()
        
    def setConsoMode(self,state):
        assert isinstance(state,bool)
        self.var.setValue('consoMode',state)

    def setDetectionMode(self,state):
        assert isinstance(state,bool)
        self.var.setValue('detectionMode',state)
        
    def setActiveUser(self,user):
        self.var.setValue('activeUser',user)
        
    def updateCapsPrice(self):
        value = self.database.getCurrentCapsValue()
        self.var.setValue('capsPrice',value)
            
            
            