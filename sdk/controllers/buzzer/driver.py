# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 22:00:39 2017

@author: pi
"""

from RPi import GPIO
import time

class Buzzer :
    
    def __init__(self):
    
        self.PIN = 40
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN, GPIO.OUT)         
        self.beepDuration=0.1 #s

 
    def setEnabled(self,state):
        
        assert isinstance(state,bool)
        if state is True:
            GPIO.output(self.PIN,1)                
        else :
            GPIO.output(self.PIN,0)

            
    def beep(self,delay=0.05):
            
        self.setEnabled(True)
        time.sleep(delay)
        self.setEnabled(False)
        


if __name__ == '__main__' :
    a = Buzzer()
    a.beep()
