# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 19:59:58 2019

@author: qchat
"""

print()
print()
print('================')
print(' COFFEE MANAGER ')
print('================')
print()
print()
print('Application starting, please wait...')
print('')


import os
import time


# Waiting for incoming connection
print('Waiting for an internet connection, please wait...',end="\r")
tini = time.time()
maxDelay = 40 #s
result = False
i = 0
while time.time()-tini < maxDelay :
    if i>100:#os.system('ping -c1 google.com') == 0 :
        result = True
        break
    else :
        i+=1
        time.sleep(0.1)
        print('Waiting for an internet connection, please wait... (%i)'%round(maxDelay-(time.time()-tini)),end="\r")
print('Connected to internet!')
print()

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