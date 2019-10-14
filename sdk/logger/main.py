#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 11:13:09 2018

@author: pi
"""

class Logger():
    
    def __init__(self,sdk):
        self.sdk = sdk
        self.print = True
        
    
    def log(self,message):
        timestamp = self.sdk.system.getTimeStamp()+': '
        if self.print is True :
            print(timestamp+message)