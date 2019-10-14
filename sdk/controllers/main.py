#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 11:13:09 2018

@author: pi
"""

from .buzzer.driver import Buzzer
from .led.driver import Led
from threading import Thread, Event
import time


class Controllers():
    
    def __init__(self,sdk):
        
        self.sdk = sdk
    
        self.led = Led()
        self.ledManager = LedManager(self)
        self.ledManager.start()
        
        self.buzzer = Buzzer()
        
    def stopThreads(self):
        self.ledManager.stopFlag.set()
        
        
        
class LedManager(Thread):

    def __init__(self,controllers):
    
        Thread.__init__(self)
        
        self.var = controllers.sdk.var
        self.led = controllers.led
        self.stopFlag = Event()
        
        self.standbyColor = 'black'
        self.currScenario = 'standby'
        
    def run(self):
    
        while self.stopFlag.is_set() is False :
            
            scenario = self.var.getValue('ledScenario')
            
            if scenario == 'standby' :
                if time.time()-self.var.getValue('awakeTime')<30 and self.standbyColor != 'white' :
                    self.led.setColorByName('white')
                    self.standbyColor = 'white'
                elif time.time()-self.var.getValue('awakeTime')>30 and self.standbyColor != 'black' :
                    self.led.setColorByName('black')
                    self.standbyColor = 'black'
                
            else :
                self.standbyColor = None
                
                if scenario == 'highBalance' and self.currScenario != scenario :
                    self.led.setColorByName('green')
                    
                if scenario == 'lowBalance' :
                    self.led.setColorByName('black',delay=0)
                    self.led.setColorByName('orange',delay=1.5)
                    self.led.setColorByName('black',delay=1.5)
                    
                if scenario == 'negativeBalance' :
                    self.led.setColorByName('black',delay=0)
                    self.led.setColorByName('red',delay=0.25)
                    self.led.setColorByName('black',delay=0.25)
                   
                
                elif scenario == 'infoMode' and self.currScenario != scenario :
                    self.led.setColorByName('black',delay=0)
                

            self.currScenario = scenario
            time.sleep(0.1)    
            
