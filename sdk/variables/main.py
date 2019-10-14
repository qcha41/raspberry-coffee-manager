# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 11:37:01 2019

@author: qchat
"""

from threading import Lock

class Variables():
    
    def __init__(self):
        
        self.var =  {'activeUser':None,
                     'email':True,
                     'image':None,
                     'rfid_time':0,
                     'rfid_tag':0,
                     'pir_time':0,
                     'awakeTime':0,
                     'ledScenario':'standby',
                     'consoMode':False,
                     'adminMode':False,
                     'adminDelay':1,
                     'detectionMode':False,
                     'detectionSignal':None,
                     'newUserDefaultDonation':0.05,
                     'capsPrice':0}
        self.lock = Lock()

    def getValue(self,name):
        assert name in self.var.keys()
        self.lock.acquire()
        value = self.var[name]
        self.lock.release()
        return value

    def setValue(self,name,value):
        assert name in self.var.keys()
        self.lock.acquire()
        self.var[name] = value
        self.lock.release()