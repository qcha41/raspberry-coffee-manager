# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 19:09:21 2018

@author: qchat
"""

import os
import numpy as np
import time
from threading import Thread


class Led :

    def __init__(self):
    
        self.PINS = {'r':1,'g':2,'b':0}
        self.config = {'r':0,'g':0,'b':0}
        self.delay_step = 0.045 #s
        self.imax = 0.9 # /1
        self.colors = {'red':(255,0,0),
                       'green':(0,255,0),
                       'white':(255,200,100),
                       'orange':(255,150,0),
                       'black':(0,0,0)}

        loaderFilePath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))),'PiBits','ServoBlaster','user')
        os.system("sudo %s/servod --p1pins=13,15,16 --step-size=2us --cycle-time=5000us"%loaderFilePath +" --min=0% --max=100%")
        
    def setColor(self,r,g,b,delay=0.5):
    
        if delay != 0 :

            nb_pts = int(round(delay / self.delay_step))
            r_list = np.linspace(self.config['r'],r,nb_pts)
            g_list = np.linspace(self.config['g'],g,nb_pts)
            b_list = np.linspace(self.config['b'],b,nb_pts)
    
            for i in range(nb_pts) :
                tini=time.time()
                w = Worker(self)
                w.setState(r_list[i],g_list[i],b_list[i])
                w.start()
                try :
                    time.sleep(self.delay_step-(time.time()-tini))
                except :
                    pass
                    
        else :
        
            w = Worker(self)
            w.setState(r,g,b)
            w.start()
            
        self.config['r']=r
        self.config['b']=b
        self.config['g']=g
        
    def setColorByName(self,name,**kwargs):
        if name in self.colors.keys():
            r,g,b = self.colors[name]
            self.setColor(r,g,b,**kwargs)
        

class Worker(Thread):

    def __init__(self,driver):
        Thread.__init__(self)
        self.imax = driver.imax
        self.pins = driver.PINS

    def setState(self,r,g,b):
        self.r = r
        self.g = g
        self.b = b

    def run(self):
        command = ''
        command += "echo %i=%.f"%(self.pins['r'],self.imax*self.r/255*100) + "% > /dev/servoblaster;"
        command += "echo %i=%.f"%(self.pins['g'],self.imax*self.g/255*100) + "% > /dev/servoblaster;"
        command += "echo %i=%.f"%(self.pins['b'],self.imax*self.b/255*100) + "% > /dev/servoblaster;"
        os.system(command)

if __name__ == '__main__' :
    a = Led()
    delay=2
    while True :
        a.setColor(255,153,102,delay)
        time.sleep(2)
        a.setColor(0,0,0,delay)
        time.sleep(1)
        

        
        

