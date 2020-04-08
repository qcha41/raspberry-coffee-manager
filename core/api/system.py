# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 21:28:16 2019

@author: qchat
"""

import os
import datetime as dt 
from urllib.request import urlopen


def shutdown():
    
    ''' Send shutdown command to shell '''
    
    os.system('sudo shutdown now')
        
    
def reboot():
    
    ''' Send reboot command to shell '''
    
    print('reboot')
    os.system('sudo shutdown -r now')
    

def awake_screen():
    
    ''' Send awake screen command to shell '''
    
    os.system("xset dpms force on")
        
  
def is_connected():
    
    ''' Returns the current connection status '''
    
    try:
        urlopen('http://google.com',timeout=1) 
        return True
    except:
        return False

    
def get_time_stamp(self):
    
    ''' Returns the current time stamp in isoformat '''
    
    return dt.datetime.now().isoformat()