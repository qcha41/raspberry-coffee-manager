# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 20:36:13 2018

@author: qchat
"""
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtCore import pyqtSignal, Qt


from PyQt5.uic import loadUi
import os
from threading import Event,active_count, enumerate
from PyQt5.QtCore import QThread
from datetime import datetime as dt
import time



class GUI(QMainWindow):

    sdkConfiguredSignal = pyqtSignal(bool)
    changeWidgetSignal = pyqtSignal(str)
    updateDateLabelSignal = pyqtSignal(str)

    
    useraccount_refreshDetailsSignal = pyqtSignal(str)
    useraccount_updateReturnTextSignal = pyqtSignal(str)
    useraccount_closePanelSignal = pyqtSignal()
    useraccount_rechargeButtonBlinkingSignal = pyqtSignal(bool)
    useraccount_emailButtonBlinkingSignal = pyqtSignal(bool)
    useraccount_updateTagSignal = pyqtSignal(str)
    useraccount_detectionSignal = pyqtSignal()
    
    accueil_updateImageSignal = pyqtSignal()
    accueil_setVisibleMessageSignal = pyqtSignal(bool)
    accueil_detectionSignal = pyqtSignal()
    
    operations_updateDetailsSignal = pyqtSignal(str,str)
    operations_refreshDetailsSignal = pyqtSignal(str)
    
    expenses_updateDetailsSignal = pyqtSignal(str)
    

    def __init__(self,sdk):
        self.sdk = sdk 
        
        QMainWindow.__init__(self)
        
        # GUI file
        self.scriptFolder = os.path.dirname(os.path.realpath(__file__))
        loadUi(os.path.join(self.scriptFolder,'main.ui'), self)
        
        # Screen setting
        self.showFullScreen()
        self.setCursor(Qt.BlankCursor)
        
		    # First widget initialization
        self.stackedWidget.setCurrentWidget(self.starting_panel)
        
		    # Signal connections
        self.sdkConfiguredSignal.connect(self.sdkConfigured)
        
        # SDK configuration procedure
        self.threads = {}
        self.threads['sdkConfig'] = SdkConfiguration(self)
        self.threads['sdkConfig'].start()
        
        
    def sdkConfigured(self,result):
        if result is True :
            self.starting_text_label.setText('Loading gui...')
            time.sleep(2)
            self.configure()
        else :
            self.starting_text_label.setText('No internet connection.\nRestarting...')
            time.sleep(2)
            self.sdk.system.restart()
        
        
    def configure(self):
        
        # Threads
        self.oldThreads = []
        
        # Mouse
        self.keyPressedFunction = None
        
        # Widgets
        from .widgets.accueil import AccueilPanel
        from .widgets.admin import AdminPanel
        from .widgets.user_account import UserAccountPanel
        from .widgets.overview import OverviewPanel
        from .widgets.keyboard import Keyboard
        from .widgets.operations import OperationsPanel
        from .widgets.expenses import ExpensesPanel
        from .widgets.donations import DonationsPanel

        self.keyboard = Keyboard(self)

        self.widgets = {'accueil':AccueilPanel(self),
                        'admin':AdminPanel(self),
                        'useraccount':UserAccountPanel(self),
                        'operations':OperationsPanel(self),
                        'expenses':ExpensesPanel(self),
                        'overview':OverviewPanel(self),
                        'donations':DonationsPanel(self)}
        
        # Signal connection
        self.updateDateLabelSignal.connect(self.updateDate)
        self.useraccount_updateReturnTextSignal.connect(self.useraccount_return_pushButton.setText)
        self.useraccount_rechargeButtonBlinkingSignal.connect(self.widgets['useraccount'].setRedRechargeButton)
        self.useraccount_emailButtonBlinkingSignal.connect(self.widgets['useraccount'].setRedEmailButton)
        self.useraccount_updateTagSignal.connect(self.useraccount_tag_label.setText)
        self.useraccount_closePanelSignal.connect(self.widgets['useraccount'].returnPushButtonClicked)
        self.useraccount_detectionSignal.connect(self.widgets['useraccount'].tagDetection)
        self.accueil_detectionSignal.connect(self.widgets['accueil'].tagDetection)
        self.accueil_updateImageSignal.connect(self.widgets['accueil'].updateImage)
        self.accueil_setVisibleMessageSignal.connect(self.accueil_passyourcard_label.setVisible)
        self.operations_updateDetailsSignal.connect(self.widgets['operations'].updateDetails)
        self.changeWidgetSignal.connect(self.changeWidget)
        self.expenses_updateDetailsSignal.connect(self.widgets['expenses'].updateDetails)
        
        
        # Date and time update thread
        self.threads['timeUpdater'] =  TimeUpdater(self)
        self.threads['timeUpdater'].start()
        
        # First widget displayed
        self.currWidget = None       
        self.changeWidget('accueil')
        
    
    
    def updateDate(self,text):
        self.date_label.setText(text)
        QApplication.processEvents()
            
    
    def mousePressEvent(self, QMouseEvent):
        try :
            self.keyPressedFunction()
        except :
            pass
    
    def changeWidget(self,name):
    
        # Fermeture widget courant
        if self.currWidget is not None :
            self.currWidget.stop()  
        
        # Demarrage nouveau widget
        self.currWidget = self.widgets[name]
        self.currWidget.start()
        self.setPanel(self.currWidget.panel)
        
    def setPanel(self,panel):
        self.stackedWidget.setCurrentWidget(panel)
        
    def toThreadBin(self,thread):
    
        if hasattr(thread,'stopFlag') :
            thread.stopFlag.set()
        self.oldThreads.append(thread)
        
        for th in self.oldThreads :
            if th.isRunning() is False :
                self.oldThreads.remove(th)

        
        
    
    def launchKeyboardRequest(self,query,mode,callback,initialValue=None,testFunction=None):
        
        # Configuration keyboard
        self.keyboard.reset()
        self.keyboard.setPreviousWidget(self.currWidget)
        self.keyboard.setQuery(query)
        self.keyboard.setCallback(callback)
        self.keyboard.setMode(mode)
        if initialValue is not None : 
            self.keyboard.updateValue(str(initialValue),len(str(initialValue)))
        if testFunction is not None :
            self.keyboard.setTestFunction(testFunction)
        self.keyboard.start()
        
        # Affichage keyboard        
        self.stackedWidget.setCurrentWidget(self.keyboard_panel)
        

        
        
class SdkConfiguration(QThread):

    def __init__(self,gui):
        QThread.__init__(self)
        self.gui = gui
        self.sdk = gui.sdk 
        
    def run(self):
        result = self.sdk.system.waitForInternet()
        self.gui.sdkConfiguredSignal.emit(result)
        
        

            
            
            
    

class TimeUpdater(QThread):

    def __init__(self,gui):
        QThread.__init__(self)
        self.gui = gui 
        self.text = ''
        self.stopFlag = Event()
        self.DELAY = 5
    
    def run(self):
        while self.stopFlag.is_set() is False :
            text = dt.today().strftime('%A\n%d/%m/%Y\n%H:%M')
            if text != self.text :
                self.text = text
                self.gui.updateDateLabelSignal.emit(text)
            time.sleep(self.DELAY)

            






class ThreadsMonitoring(QThread):

    def __init__(self):
        QThread.__init__(self)
        self.stopFlag = Event()
    
    def run(self):
        while self.stopFlag.is_set() is False :
            print('number of threads :',active_count())
            for a in enumerate() :
                print(type(a),id(a))
            time.sleep(1)
        
#a = ThreadsMonitoring()
#a.start()
