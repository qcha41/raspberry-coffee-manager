# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 20:36:13 2018

@author: qchat
"""
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.uic import loadUi
from PyQt5.QtCore import QThread

from .widgets.startup import StartupPanel
from .widgets.main import MainPanel
from .widgets.account import AccountPanel
from .widgets.account_setup import AccountSetupPanel
from .widgets.new_user import NewUserPanel
from .widgets.keyboard import KeyboardPanel
from .widgets.stats import StatsPanel
from .widgets.admin import AdminPanel

import os
from threading import Event,active_count, enumerate
from datetime import datetime as dt
import time

class GUI(QMainWindow):

    switch_panel_signal = pyqtSignal(str)
    
#    useraccount_updateReturnTextSignal = pyqtSignal(str)
#    useraccount_closePanelSignal = pyqtSignal()
#    useraccount_rechargeButtonBlinkingSignal = pyqtSignal(bool)
#    useraccount_emailButtonBlinkingSignal = pyqtSignal(bool)
#    useraccount_updateTagSignal = pyqtSignal(str)
#    useraccount_detectionSignal = pyqtSignal()
#    
#    accueil_updateImageSignal = pyqtSignal()
#    accueil_setVisibleMessageSignal = pyqtSignal(bool)
#    accueil_detectionSignal = pyqtSignal()
#    
#    operations_updateDetailsSignal = pyqtSignal(str,str)
#    operations_refreshDetailsSignal = pyqtSignal(str)
#    
#    expenses_updateDetailsSignal = pyqtSignal(str)
    

    def __init__(self):
        
        QMainWindow.__init__(self)
        
        # GUI file
        loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)),'main.ui'), self)
        
        # Screen setting
        #self.showFullScreen()
        #self.setCursor(Qt.BlankCursor)
        
        # Connect signals
        self.switch_panel_signal.connect(self.switch_panel)
        
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
        self.send_email = False
        
        # Initialize by waiting for internet
        self.switch_panel('startup')
#        
#        # SDK configuration procedure
#        self.threads = {}
#        self.threads['sdkConfig'] = SdkConfiguration(self)
#        self.threads['sdkConfig'].start()
        
#        
#    def sdkConfigured(self,result):
#        if result is True :
#            self.starting_text_label.setText('Loading gui...')
#            time.sleep(2)
#            self.configure()
#        else :
#            self.starting_text_label.setText('No internet connection.\nRestarting...')
#            time.sleep(2)
#            self.sdk.system.restart()
#        
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
        
        # Exit
        event.accept()
        




class Countdown():
    
    def __init__(self):
        
        self.timer_main = QTimer()
        self.timer_sec = QTimer()  
        
        self.timer_main.setSingleShot(True)
        self.interval = 30

        self.callback_end = None
        self.callback_update = None
        
        self.timer_main.timeout.connect(self.end_signal_emitted)
        self.timer_sec.timeout.connect(self.update_signal_emitted)
        
    def start(self):
        
        ''' Start the countdown '''
        
        self.timer_main.start(self.interval*1000)
        self.timer_sec.start(1000)
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
        
      
        

        
#    def configure(self):
#        
#        # Threads
#        self.oldThreads = []
#        
#        # Mouse
#        self.keyPressedFunction = None
#        
#        # Widgets
#        from .widgets.startup import StartupPanel
        #from .widgets.accueil import AccueilPanel
#        from .widgets.admin import AdminPanel
#        from .widgets.user_account import UserAccountPanel
#        from .widgets.overview import OverviewPanel
#        from .widgets.keyboard import Keyboard
#        from .widgets.operations import OperationsPanel
#        from .widgets.expenses import ExpensesPanel
#        from .widgets.donations import DonationsPanel
#
#        self.keyboard = Keyboard(self)
#
#        self.widgets = {'accueil':AccueilPanel(self),
#                        'admin':AdminPanel(self),
#                        'useraccount':UserAccountPanel(self),
#                        'operations':OperationsPanel(self),
#                        'expenses':ExpensesPanel(self),
#                        'overview':OverviewPanel(self),
#                        'donations':DonationsPanel(self)}
#        
#        # Signal connection
#        self.updateDateLabelSignal.connect(self.updateDate)
#        self.useraccount_updateReturnTextSignal.connect(self.useraccount_return_pushButton.setText)
#        self.useraccount_rechargeButtonBlinkingSignal.connect(self.widgets['useraccount'].setRedRechargeButton)
#        self.useraccount_emailButtonBlinkingSignal.connect(self.widgets['useraccount'].setRedEmailButton)
#        self.useraccount_updateTagSignal.connect(self.useraccount_tag_label.setText)
#        self.useraccount_closePanelSignal.connect(self.widgets['useraccount'].returnPushButtonClicked)
#        self.useraccount_detectionSignal.connect(self.widgets['useraccount'].tagDetection)
#        self.accueil_detectionSignal.connect(self.widgets['accueil'].tagDetection)
#        self.accueil_updateImageSignal.connect(self.widgets['accueil'].updateImage)
#        self.accueil_setVisibleMessageSignal.connect(self.accueil_passyourcard_label.setVisible)
#        self.operations_updateDetailsSignal.connect(self.widgets['operations'].updateDetails)
#        self.changeWidgetSignal.connect(self.changeWidget)
#        self.expenses_updateDetailsSignal.connect(self.widgets['expenses'].updateDetails)
#        
#        
#        # Date and time update thread
#        self.threads['timeUpdater'] =  TimeUpdater(self)
#        self.threads['timeUpdater'].start()
#        
#        # First widget displayed
#        self.currWidget = None       
#        self.changeWidget('accueil')
#        
#    


#            
#    
#    def mousePressEvent(self, QMouseEvent):
#        try :
#            self.keyPressedFunction()
#        except :
#            pass
#    

#        
#    def setPanel(self,panel):
#        self.stackedWidget.setCurrentWidget(panel)
#        
#    def toThreadBin(self,thread):
#    
#        if hasattr(thread,'stopFlag') :
#            thread.stopFlag.set()
#        self.oldThreads.append(thread)
#        
#        for th in self.oldThreads :
#            if th.isRunning() is False :
#                self.oldThreads.remove(th)
#
#        
#        
#    
#    def launchKeyboardRequest(self,query,mode,callback,initialValue=None,testFunction=None):
#        
#        # Configuration keyboard
#        self.keyboard.reset()
#        self.keyboard.setPreviousWidget(self.currWidget)
#        self.keyboard.setQuery(query)
#        self.keyboard.setCallback(callback)
#        self.keyboard.setMode(mode)
#        if initialValue is not None : 
#            self.keyboard.updateValue(str(initialValue),len(str(initialValue)))
#        if testFunction is not None :
#            self.keyboard.setTestFunction(testFunction)
#        self.keyboard.start()
#        
#        # Affichage keyboard        
#        self.stackedWidget.setCurrentWidget(self.keyboard_panel)
#        
#
#        
#        

#        
#
#            
#            
#            
#    
#

#
#            
#
#
#
#
#
#
#class ThreadsMonitoring(QThread):
#
#    def __init__(self):
#        QThread.__init__(self)
#        self.stopFlag = Event()
#    
#    def run(self):
#        while self.stopFlag.is_set() is False :
#            print('number of threads :',active_count())
#            for a in enumerate() :
#                print(type(a),id(a))
#            time.sleep(1)
        
#a = ThreadsMonitoring()
#a.start()

