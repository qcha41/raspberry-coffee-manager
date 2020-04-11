# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 11:48:28 2020

@author: qchat
"""

import threading 
import time

class ThreadsMonitoring(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_flag = threading.Event()
        
    def stop(self):
        self.stop_flag.set()
    
    def run(self):
        while self.stopFlag.is_set() is False :
            print('number of threads :',threading.active_count())
            for a in threading.enumerate() :
                print(type(a),id(a))
            time.sleep(1)
        
