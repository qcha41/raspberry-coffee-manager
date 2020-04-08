# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 12:19:34 2020

@author: qchat
"""

from PyQt5.QtCore import QThread, pyqtSignal
from threading import Event
import time

from ...api import system

class StartupPanel() :
    
    def __init__(self,gui) :
        
        self.gui = gui
        self.thread = None
        
        # Connect buttons
        self.gui.startup_reboot_pushButton.clicked.connect(system.reboot)
        self.gui.startup_closeApp_pushButton.clicked.connect(self.gui.close)
        
        
        
    def start(self):

        # Wait for internet
        self.thread = WaitForInternetThread()
        self.thread.connected_signal.connect(self.connection_established)
        self.thread.start()
        
        
    def stop(self):
        if self.thread is not None :
            self.thread.stop_flag.set()
            self.thread = None
        
    def connection_established(self):
        self.gui.switch_panel_signal.emit('main')
        self.gui.update_datetime()
        
        
        
        
class WaitForInternetThread(QThread):
    
    connected_signal = pyqtSignal()
        
    def __init__(self):
        QThread.__init__(self)
        self.stop_flag = Event()
        
    def run(self):
        
        while self.stop_flag.is_set() is False : 
            
            if system.is_connected() is True :
                self.connected_signal.emit()
                break
            
            time.sleep(1)
    
#        
        
        