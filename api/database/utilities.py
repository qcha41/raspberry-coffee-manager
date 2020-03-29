# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 20:49:42 2020

@author: qchat
"""

import datetime as dt

def get_current_year():
    
    ''' Returns current year '''
    
    return dt.datetime.now().year
    
    
def get_timestamp():
    
    ''' Returns current timestamp '''
    
    return dt.datetime.now().isoformat() 