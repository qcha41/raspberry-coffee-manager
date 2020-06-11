#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 11:13:09 2018

@author: pi
"""



from .. import config
from .. import system 

import os

class DeviceManager():
    
    def __init__(self):
        
        from .buzzer_lib import BuzzerController
        from .led_lib import LedController
        from .pir_lib import PirSensor
        from .rfid_lib import RfidReader
        
        # Led controller
        current_script_path = os.path.realpath(os.path.dirname(__file__))
        pibits_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_script_path)))),'PiBits')

        gpio_pin_red_led = int(config['DEVICES']['gpio_pin_red_led'])
        gpio_pin_green_led = int(config['DEVICES']['gpio_pin_green_led'])
        gpio_pin_blue_led = int(config['DEVICES']['gpio_pin_blue_led'])        
        self.led = LedController(pibits_path, gpio_pin_red_led, gpio_pin_green_led, gpio_pin_blue_led)
        self.led.start()
        
        # Buzzer controller
        gpio_pin_buzzer = int(config['DEVICES']['gpio_pin_buzzer'])
        self.buzzer = BuzzerController(gpio_pin_buzzer)
        
        # PIR sensor
        gpio_pin_pir = int(config['DEVICES']['gpio_pin_pir'])
        self.pir = PirSensor(gpio_pin_pir)
        self.pir.callback = self.wake_up
        
        # RFIF reader
        self.rfid = RfidReader()
        self.rfid.start()
        
    def stop(self):
        
        self.led.stop()
        self.rfid.stop()
        
    def wake_up(self):
        
        self.led.set_idle_color('white')
        system.awake_screen()