# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 20:36:13 2018

@author: qchat
"""
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.uic import loadUi

from .widgets.startup import StartupPanel
from .widgets.main import MainPanel
from .widgets.account import AccountPanel
from .widgets.account_setup import AccountSetupPanel
from .widgets.new_user import NewUserPanel
from .widgets.keyboard import KeyboardPanel
from .widgets.stats import StatsPanel
from .widgets.admin import AdminPanel

import os
from datetime import datetime as dt

from ..api.devices import devices

class GUI(QMainWindow):

    switch_panel_signal = pyqtSignal(str)
    rfid_tag_detected_signal = pyqtSignal(str)

    def __init__(self):
        
        QMainWindow.__init__(self)
        
        # GUI file
        loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)),'main.ui'), self)
        
        # Screen setting
        self.showFullScreen()
        self.setCursor(Qt.BlankCursor)
        
        # Connect signals
        self.switch_panel_signal.connect(self.switch_panel)
        devices.rfid.signal = self.rfid_tag_detected_signal
        
        # Countdown thread
        self.countdown = Countdown()
		
        # Load widgets
        self.widgets = {}
        self.widgets['startup'] = StartupPanel(self)
        self.widgets['main'] = MainPanel(self)
        self.widgets['account'] = AccountPanel(self)
        self.widgets['account_setup'] = AccountSetupPanel(self)
        self.widgets['new_user'] = NewUserPanel(self)
        self.widgets['keyboard'] = KeyboardPanel(self)
        self.widgets['stats'] = StatsPanel(self)
        self.widgets['admin'] = AdminPanel(self)
        
        self.current_widget = None
        
        # Start datetime updater
        self.time_datetime = QTimer()
        self.time_datetime.setInterval(60000)
        self.time_datetime.timeout.connect(self.update_datetime)
        self.time_datetime.start()
        self.update_datetime()
        
        # Current user selected
        self.current_user = None
        
        # Send email state
        self.send_email = True
        
        # Initialize by waiting for internet
        self.switch_panel('startup')
   
#
        
    def update_datetime(self):
        
        datetime = dt.today().strftime('%A\n%d/%m/%Y\n%H:%M')
        self.date_label.setText(datetime)
        
        
    def mousePressEvent(self, QMouseEvent):
        
        ''' Reset countdown if running when mouse click detected '''
        
        if self.countdown.is_active() :
            self.countdown.start()
            

    def switch_panel(self,panel_name):
        
        ''' Close properly current panel and open the given one '''
        
        # Reset countdown
        self.countdown.stop()
        self.countdown.callback_end = None
        self.countdown.callback_update = None
        
        # Terminate current widget
        if self.current_widget is not None :
            self.current_widget.stop()  
        
        # Initialization new widget
        self.current_widget = self.widgets[panel_name]
        if hasattr(self.current_widget,'callback_countdown_end') : 
            self.countdown.callback_end = self.current_widget.callback_countdown_end
        if hasattr(self.current_widget,'callback_countdown_update') : 
            self.countdown.callback_update = self.current_widget.callback_countdown_update
        self.current_widget.start()
        self.stackedWidget.setCurrentWidget(getattr(self,panel_name+'_panel'))
        
        
    def closeEvent(self, event):
        
        ''' Prepare the GUI to close '''
        
        # Terminate timers
        self.countdown.stop()
        self.time_datetime.stop()
        
        # Terminate others threads
        if self.current_widget is not None :
            self.current_widget.stop()
        
        # Terminate api threads
        devices.stop()
        
        # Exit
        event.accept()
        
        # Close python
        pid = os.system('pgrep python')
        os.system('sudo kill -sigterm %i'%pid) 




class Countdown():
    
    def __init__(self):
        
        self.timer_main = QTimer()
        self.timer_sec = QTimer()  
        
        self.timer_main.setSingleShot(True)
        self.interval = 30
        self.timer_sec.setInterval(1000)

        self.callback_end = None
        self.callback_update = None
        
        self.timer_main.timeout.connect(self.end_signal_emitted)
        self.timer_sec.timeout.connect(self.update_signal_emitted)
        
    def start(self):
        
        ''' Start the countdown '''
        
        self.timer_main.start(self.interval*1000)
        self.timer_sec.start()
        self.update_signal_emitted()
        
        
    def end_signal_emitted(self):
        
        ''' Stop countdown and run callback_end function '''
        
        self.stop()
        if self.callback_end is not None : 
            self.callback_end()
        
        
    def update_signal_emitted(self):
        
        ''' Run callback_update function '''
        
        if self.callback_update is not None :
            remaining_time = self.timer_main.remainingTime()
            if remaining_time != -1 : 
                self.callback_update(int(round(remaining_time/1000)))
    
    
    def stop(self):
        
        ''' Stop the countdown '''
        
        self.timer_main.stop()
        self.timer_sec.stop()
        
        
    def is_active(self):
        
        ''' Returns the state of the countdown '''
        
        return self.timer_main.isActive()
        
      
        
