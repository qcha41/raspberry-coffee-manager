# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 21:28:16 2019

@author: qchat
"""

import os
import datetime as dt 
import time,sys


class System():
    
    def __init__(self,sdk):
        self.sdk = sdk
    

    def shutdown(self):
        os.system('sudo shutdown now')
            
    def restart(self):
        os.system('sudo shutdown -r now')
        
    def close(self):
        #self.sdk.stopThreads()
        pid = os.system('pgrep python3')
        os.system('sudo kill -sigterm %i'%pid) 
    
    def awake(self):
        os.system("xset dpms force on") # Screen 
        self.sdk.var.setValue('awakeTime',time.time()) # LEDs
        
      
    def isConnected(self):
        return os.system('ping -c1 google.com') == 0
        
    def waitForInternet(self): 
    
        self.sdk.setDetectionMode(True)
        
        tini = time.time()
        maxDelay = 40 #s
        
        result = False
        while time.time()-tini < maxDelay :
            
            if self.isConnected() or self.sdk.var.getValue('adminMode') is True :
                result = True
                break
                
        self.sdk.setDetectionMode(False)
        
        return result
    
    
        
        
    def getTimeStamp(self):
        return dt.datetime.now().isoformat()