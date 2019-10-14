# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 19:09:21 2018

@author: qchat
"""

from RPi import  GPIO

class PirSensor :
    def __init__(self,callback):

        self.PIN = 31
        self.callback = callback

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN,GPIO.IN)
        
        GPIO.add_event_detect(self.PIN,GPIO.RISING,callback=self.callback,bouncetime=1)
        
    def getCurrentState(self):
        return GPIO.input(self.PIN)
    

        
        
if __name__ == '__main__' :

    a = PirSensor()
    def event(o):
        print(GPIO.input(a.PIN))
        
    #GPIO.add_event_detect(6,GPIO.BOTH,callback=event)
    while True :
        print(GPIO.input(a.PIN))

