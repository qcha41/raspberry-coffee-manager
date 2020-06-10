# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 19:09:21 2018

@author: qchat
"""

import os
import numpy as np
import time
from threading import Thread, Event
from queue import Queue



colors = {'red':(255,0,0),
          'green':(0,255,0),
          'white':(255,200,100),
          'orange':(255,150,0),
          'black':(0,0,0)}

class LedController(Thread):
    
    def __init__(self,pibits_path, gpio_pin_red_led, gpio_pin_green_led, gpio_pin_blue_led) :
        
        Thread.__init__(self)
        
        self.pins = {'red':gpio_pin_red_led,
                     'green':gpio_pin_green_led,
                     'blue':gpio_pin_blue_led}
        
        self.curr_scenario = 'idle'
        self.curr_color = 'black'
        self.idle_color = 'black'
        self.idle_last_change_time = time.time()
        self.idle_color_autoswitch_delay = 30 #s

        self.imax = 0.9
        self.delay_step = 0.045 #s
        
        self.queue = Queue()
        self.stop_flag = Event()

        self.pibits_path = pibits_path
        servod_folder_path = os.path.join(self.pibits_path,'ServoBlaster','user')
        os.system(f"sudo {servod_folder_path}/servod --p1pins={self.pins['red']},{self.pins['green']},{self.pins['blue']} --step-size=2us --cycle-time=5000us --min=0% --max=100%")
        
        
        
    def set_scenario(self,scenario):
        
        self.curr_scenario = scenario
        if scenario == 'idle' :
            self.ilde_last_change_time = time.time()
        
    def set_idle_color(self,color):
        
        self.idle_color = color
        self.ilde_last_change_time = time.time()

    def stop(self):
        self.stop_flag.set()
        self.join()

    def run(self):
        
        while self.stop_flag.is_set() is False :

            if self.curr_scenario == 'idle' :
                if self.idle_color != 'black' and (time.time()-self.idle_last_change_time)>self.idle_color_autoswitch_delay :
                    self.idle_color = 'black'
                self.apply_color(self.idle_color,0.5)
            if self.curr_scenario == 'fixed_green' :
                self.apply_color('green',0.5)
            if self.curr_scenario == 'low_blinking_orange' :
                self.apply_color('orange', 1.5) 
                self.apply_color('black',1.5) 
            if self.curr_scenario == 'high_blinking_red' :
                self.apply_color('red',0.2) 
                self.apply_color('black',0.2)
            
    
    

    def apply_color(self,color,delay):
        
        print('pass')
        
        if color == self.curr_color :
            time.sleep(delay)
            
        else :             
            (curr_r,curr_g,curr_b) = colors[self.curr_color]
            (new_r,new_g,new_b) = colors[color]
            
            # Setup sequence
            nb_pts = int(round(delay / self.delay_step)+2)
            r_list = np.linspace(curr_r,new_r,nb_pts)
            g_list = np.linspace(curr_g,new_g,nb_pts)
            b_list = np.linspace(curr_b,new_b,nb_pts)
            
            # Execute sequence
            for i in range(len(r_list)) :
                tini = time.time()
                command = ''
                command += f"echo P1-{self.pins['red']}={round(self.imax*r_list[i]/255*100,2)}% > /dev/servoblaster;"
                command += f"echo P1-{self.pins['green']}={round(self.imax*g_list[i]/255*100,2)}% > /dev/servoblaster;"
                command += f"echo P1-{self.pins['blue']}={round(self.imax*b_list[i]/255*100,2)}% > /dev/servoblaster;"
                os.system(command)
                time.sleep(self.delay_step-(time.time()-tini))
            
            # Save last state
            self.color = color

        

        
if __name__ == '__main__' :
    
    pibits_path = ''
    gpio_pin_red_led = 15
    gpio_pin_green_led = 16
    gpio_pin_blue_led = 13
    
    led = LedController(pibits_path, gpio_pin_red_led, gpio_pin_green_led, gpio_pin_blue_led)
    led.set_scenario('high_blinking_red')
    time.sleep(3)
    led.set_scenario('high_blinking_red')
    
 
        




