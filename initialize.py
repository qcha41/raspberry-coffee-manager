# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 19:59:58 2019

@author: qchat
"""
import os
import time

tini = time.time()
maxDelay = 40

print('coucou')
print('coucou')
        

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