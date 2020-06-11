# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 22:00:39 2017

@author: pi
"""

from RPi import GPIO
import time

class BuzzerController :
    
    def __init__(self,gpio_pin):
    
        self.pin = gpio_pin
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)    
        
 
    def setEnabled(self,state):
        
        ''' Start or stop buzzer '''
        
        assert isinstance(state,bool)
        GPIO.output(self.pin,int(state))  


    def beep(self,delay):
        
        ''' Produce a beep during <delay> seconds '''
        
        self.setEnabled(True)
        time.sleep(delay)
        self.setEnabled(False)
        
            
    def short_beep(self):
        
        ''' Produce a short beep '''
        
        self.beep(0.05)
        
        
    def long_beep(self):
        
        ''' Produce a long beep '''
        
        self.beep(0.5)
        


if __name__ == '__main__' :
    a = BuzzerController(40)
    a.short_beep()
    time.sleep(0.2)
    a.long_beep()
