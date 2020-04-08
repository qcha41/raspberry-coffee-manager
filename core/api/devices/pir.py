# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 19:09:21 2018

@author: qchat
"""

from RPi import  GPIO

class PirSensor :
    
    def __init__(self,gpio_pin):

        self.PIN = gpio_pin
        self.callback = None

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN,GPIO.IN)
        
        GPIO.add_event_detect(self.PIN,GPIO.RISING,callback=self.event_detected,bouncetime=1)
        
    def event_detected(self):
        if self.callback is not None : self.callback()
        
    def get_current_state(self):
        return GPIO.input(self.PIN)
    

        
        
if __name__ == '__main__' :
    
    def event(o):
        print('Event callback ', GPIO.input(a.PIN))

    a = PirSensor(31)
    a.callback = event
    
    while True :
        print(a.get_current_state())

