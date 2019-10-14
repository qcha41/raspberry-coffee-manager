# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 20:36:13 2018

@author: qchat
"""

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread

import time
from threading import Event





class AccueilPanel :

    
    
    def __init__(self,gui):
    
        self.gui=gui
        self.sdk=gui.sdk
        self.panel = self.gui.accueil_panel
        self.threads = {}
        
        self.gui.accueil_info_pushButton.pressed.connect(self.infoButtonStateChanged)
        self.gui.accueil_info_pushButton.released.connect(self.infoButtonStateChanged)
        
        self.gui.accueil_passyourcard_label.setStyleSheet("color: red")
        
        self.newUserTag = 0
        
        
        
    def start(self):
        
        self.gui.keyPressedFunction = self.forceImageUpdate
        
        donation = self.sdk.database.getUsersDonationValue()
        self.gui.accueil_donation_label.setText('Donation\n%.2f \u20ac'%donation)
        
        capsPrice = self.sdk.var.getValue('capsPrice')
        self.gui.accueil_capsprice_label.setText('Caps price\n%.2f \u20ac'%capsPrice)
        
        self.threads['passYourCardBlinking'] = PassYourCardBlinking(self)
        self.threads['passYourCardBlinking'].start()
        self.threads['imageUpdater'] = ImageUpdater(self)
        self.threads['imageUpdater'].start()
        
        self.gui.accueil_info_pushButton.setStyleSheet('font: bold 28px')
        
        self.sdk.setDetectionMode(True)
        self.sdk.setConsoMode(True)
        
        self.sdk.var.setValue('detectionSignal',self.gui.accueil_detectionSignal)
    
    
    def stop(self):
        for name in self.threads.keys() :
            self.gui.toThreadBin(self.threads[name])
        self.threads = {}
        self.sdk.setConsoMode(False)
        self.sdk.setDetectionMode(False)
        self.sdk.var.setValue('detectionSignal',None)
        


    def tagDetection(self):
        if self.sdk.var.getValue('adminMode') is True :
            self.gui.changeWidgetSignal.emit('admin')
        else :
            if self.sdk.var.getValue('activeUser') is not None :
                self.gui.changeWidgetSignal.emit('useraccount')
            else :
                self.newUserTag = self.sdk.var.getValue('rfid_tag')
                self.gui.launchKeyboardRequest("Enter your name:",
                                              str,self.setNewUser,testFunction=self.checkName)
                
    def renameButtonPressed(self):
        username = self.sdk.database.getUserName(self.user)
        self.gui.launchKeyboardRequest("Update %s's name:"%username,
                                       str,self.setName,initialValue=username,testFunction=self.checkName)
        
    def checkName(self,value):
        if value is not None and value not in self.sdk.database.getUserNameList() :
            return True
        else :
            return False
            
    def setNewUser(self,name):
        if name is not None :
            self.sdk.database.newUser(name)
            user = self.sdk.database.getUserByName(name)
            self.sdk.database.setUserTag(user,self.newUserTag)
            self.sdk.email.newUser(name)




    def forceImageUpdate(self):
        self.threads['imageUpdater'].stopFlag.set()
        self.gui.toThreadBin(self.threads['imageUpdater'])
        self.threads['imageUpdater'] = ImageUpdater(self)
        self.threads['imageUpdater'].start()
        
    def updateImage(self):
        pixmap = self.sdk.var.getValue('image')
        self.gui.accueil_image_label.setPixmap(pixmap)
    
    
    
    
    
    
    def infoButtonStateChanged(self):
        state = self.gui.accueil_info_pushButton.isDown()
        if state is True :
            self.sdk.setConsoMode(False)
            self.sdk.var.setValue('ledScenario','infoMode')
            self.gui.accueil_info_pushButton.setStyleSheet('background-color: green;font: bold 28px')
        else :
            self.gui.accueil_info_pushButton.setStyleSheet('font: bold 28px')
            if self.gui.currWidget == self :
                self.sdk.var.setValue('ledScenario','standby')
                self.sdk.setConsoMode(True)
                






class PassYourCardBlinking(QThread):

    def __init__(self,window):
        QThread.__init__(self)
        self.gui = window.gui 
        self.stopFlag = Event()
        self.state = False
    
    def run(self):
        while self.stopFlag.is_set() is False :
            self.state = not self.state
            self.gui.accueil_setVisibleMessageSignal.emit(self.state)
            time.sleep(1)
            
            
        
class ImageUpdater(QThread):
    
    def __init__(self,widget):
        QThread.__init__(self)
        self.sdk = widget.sdk
        self.gui = widget.gui  
        self.stopFlag = Event()
        self.delay = 15 #sec
        
    def run(self):
        while self.stopFlag.is_set() is False :
            imagePath = self.sdk.images.getRandomImagePath(folder=None)
            pixmap = QPixmap(imagePath)
            if pixmap.isNull() is False :
                pixmap = pixmap.scaledToHeight(self.gui.accueil_image_label.frameGeometry().height())
                self.sdk.var.setValue('image',pixmap)
                self.gui.accueil_updateImageSignal.emit()
                time.sleep(self.delay)
            time.sleep(0.1)
        
