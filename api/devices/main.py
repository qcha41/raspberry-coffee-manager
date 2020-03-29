#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 11:13:09 2018

@author: pi
"""



from .. import config


class DeviceManager():
    
    def __init__(self):
        
        from .buzzer import BuzzerController
        from .led import LedController
        from .pir import PirSensor
        from .rfid import RfidReader
        
        # Led controller
        pibits_path = config['DEVICES']['pibits_path']
        gpio_pin_red_led = int(config['DEVICES']['gpio_pin_red_led'])
        gpio_pin_green_led = int(config['DEVICES']['gpio_pin_green_led'])
        gpio_pin_blue_led = int(config['DEVICES']['gpio_pin_blue_led'])        
        self.led = LedController(pibits_path, gpio_pin_red_led, gpio_pin_green_led, gpio_pin_blue_led)
        
        # Buzzer controller
        gpio_pin_buzzer = int(config['DEVICES']['gpio_pin_buzzer'])
        self.buzzer = BuzzerController(gpio_pin_buzzer)
        
        # PIR sensor
        gpio_pin_pir = int(config['DEVICES']['gpio_pin_pir'])
        self.pir = PirSensor(gpio_pin_pir)
        self.pir.callback = lambda : self.led.set_idle_color('white') 
        
        # RFIF reader
        self.rfid = RfidReader()
        
    def stop(self):
        
        self.led.stop()
        self.rfid.stop()