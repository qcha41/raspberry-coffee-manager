# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 19:09:21 2018

@author: qchat
"""

from .pir.driver import PirSensor
from .rfid.driver import RfidReader
import time
from threading import Thread, Event

class Sensors():
    
    def __init__(self,sdk):
    
        self.sdk = sdk

        self.rfid = RfidReader(self.rfidDetection)       
        self.pir = PirSensor(self.pirDetection)
        
        self.adminModeDisablerThread = None
        

        
    def pirDetection(self,a):
        self.sdk.var.setValue('pir_time',time.time())
        self.sdk.system.awake()

    def rfidDetection(self,tag):
        
        self.sdk.var.setValue('rfid_time',time.time())
        self.sdk.var.setValue('rfid_tag',tag)
        self.sdk.system.awake()
        
        detectionMode = self.sdk.var.getValue('detectionMode')
        if detectionMode is True :
  
            # Existing user
            if tag in self.sdk.database.getUserTagList() :
            
                user = self.sdk.database.getUserByTag(tag)
                self.sdk.setActiveUser(user)
            
                consoMode = self.sdk.var.getValue('consoMode')
                if consoMode is True : 
                    self.sdk.addConso(user)
                
                signal = self.sdk.var.getValue('detectionSignal')
                if signal is not None :
                    signal.emit()
                
                
            # Admin
            elif tag == 136419410438 :
                self.sdk.var.setValue('adminMode',True)
                if self.adminModeDisablerThread is not None :
                    self.adminModeDisablerThread.stopFlag.set()
                self.adminModeDisablerThread = AutoAdminModeDisabler(self.sdk)
                self.adminModeDisablerThread.start()
                signal = self.sdk.var.getValue('detectionSignal')
                if signal is not None :
                    signal.emit()
                
            # New user
            else :
                self.sdk.setActiveUser(None)
                signal = self.sdk.var.getValue('detectionSignal')
                if signal is not None :
                    signal.emit()
                
    def stopThreads(self):
        self.rfid.stopThread()
                
class AutoAdminModeDisabler(Thread) :
    
    def __init__(self,sdk):
        Thread.__init__(self)
        self.sdk = sdk
        self.stopFlag = Event()
        
    def run(self):
        delay = self.sdk.var.getValue('adminDelay')
        time.sleep(delay)
        self.sdk.var.setValue('adminMode',False)
                
                

        