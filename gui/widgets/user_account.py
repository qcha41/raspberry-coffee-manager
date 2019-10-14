# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 20:36:13 2018

@author: qchat
"""

from PyQt5.QtCore import QThread
import time
from threading import Event
import datetime as dt
import pandas as pd


class UserAccountPanel :

    

    def __init__(self,gui):
      
        self.gui=gui
        self.sdk=gui.sdk
        self.panel = self.gui.useraccount_panel
        self.threads = {}
        self.user = None
        self.date = None
        self.gui.useraccount_return_pushButton.clicked.connect(self.returnPushButtonClicked)
        self.gui.useraccount_previousDate_pushButton.clicked.connect(self.previousDateButtonPressed)
        self.gui.useraccount_nextDate_pushButton.clicked.connect(self.nextDateButtonPressed)
        self.gui.useraccount_recharge_pushButton.clicked.connect(self.rechargeButtonPressed)
        self.gui.useraccount_rename_pushButton.clicked.connect(self.renameButtonPressed)
        self.gui.useraccount_tag_pushButton.clicked.connect(self.tagButtonPressed)
        self.gui.useraccount_conso_pushButton.clicked.connect(self.consoButtonPressed)
        self.gui.useraccount_email_pushButton.clicked.connect(self.emailButtonPressed)
        self.gui.useraccount_refreshDetailsSignal.connect(self.gui.useraccount_details_textEdit.setHtml)
        self.gui.useraccount_donationDecrease_pushButton.clicked.connect(self.donationDecreaseButtonPressed)
        self.gui.useraccount_donationIncrease_pushButton.clicked.connect(self.donationIncreaseButtonPressed)
        
        self.setRedRechargeButton(False)
        
        
    def updateBalance(self):
        balance = round(self.sdk.database.getUserBalance(self.user),2)
        self.gui.useraccount_balance_label.setText('%g \u20ac'%(balance+0))
        
        # Activation du reminder 1
        if balance < 0 :
            self.threads['warning'] = BlinkingWarning(self)
            self.threads['warning'].start()
            self.sdk.var.setValue('ledScenario','negativeBalance')
        elif 0<=balance<10 :
            self.gui.useraccount_recharge_pushButton.setStyleSheet('background-color: orange; font: bold 30px')
            self.gui.useraccount_balance_label.setStyleSheet('color: orange; font: 40px')
            self.sdk.var.setValue('ledScenario','lowBalance')
        else :
            self.gui.useraccount_recharge_pushButton.setStyleSheet('background-color: green; font: bold 30px')
            self.gui.useraccount_balance_label.setStyleSheet('color: green; font: 40px')
            self.sdk.var.setValue('ledScenario','highBalance')
        

    
    def start(self):
        
        # Reset
        self.gui.keyPressedFunction = self.resetAutoclose
        self.data = None
        self.gui.useraccount_details_textEdit.setHtml('')
        
        # Récupération active user
        self.user = self.sdk.var.getValue('activeUser')
        
        # Display his name
        username = self.sdk.database.getUserName(self.user)
        nbCapsToday = self.sdk.database.getNbCapsToday(self.user)
        self.gui.useraccount_username_label.setText(username+' : %i caps today'%nbCapsToday)
        
        # Display his balance
        self.updateBalance()        
        
            
        # Activation du reminder 2
        currEmail = self.sdk.database.getUserEmail(self.user)
        if currEmail is None or '@' not in currEmail or currEmail[0] == '@' :
            self.threads['email'] = BlinkingEmail(self)
            self.threads['email'].start()
        
        # Désactivation mode admin        
        self.gui.useraccount_rename_pushButton.setVisible(False)
        self.gui.useraccount_tag_pushButton.setVisible(False)
        self.gui.useraccount_tag_label.setVisible(False)
        

        # Lancement des threads    
        self.threads['autoclose'] = Autoclose(self,10)
        self.threads['autoclose'].start()
        
        # Update date and then details
        self.date = self.getDateToday()
        self.updateDate()
        
        # Display donation
        self.updateDonation()
        
        # Display total donation
        totalDonation = round(self.sdk.database.getUserTotalDonation(self.user),2)
        self.gui.useraccount_totalDonationValue_label.setText('%g \u20ac'%(totalDonation+0))
        
        # Activation detection signal
        self.sdk.var.setValue('detectionSignal',self.gui.useraccount_detectionSignal)
        self.sdk.setDetectionMode(True)
        
        
    def stop(self):
        self.sdk.var.setValue('ledScenario','standby')
        self.gui.keyPressedFunction = None
        for name in self.threads.keys() :
            self.gui.toThreadBin(self.threads[name])
        self.threads = {}
        self.sdk.setDetectionMode(False)
        self.sdk.var.setValue('detectionSignal',None)
        
        
        
        
    def tagDetection(self):
        if self.sdk.var.getValue('adminMode') is True :
            self.resetAutoclose()
            self.enableAdminMode()
            self.sdk.setDetectionMode(False)
            self.sdk.var.setValue('detectionSignal',None)
    
    
    
    def resetAutoclose(self):
        self.stopAutoclose()
        self.threads['autoclose'] = Autoclose(self,30)
        self.threads['autoclose'].start()
        
        
        
    def stopAutoclose(self):
        self.gui.toThreadBin(self.threads['autoclose'])
        
        

        
    def returnPushButtonClicked(self):
        self.gui.changeWidgetSignal.emit('accueil')  
        
        
     
  
        
         
        
    def rechargeButtonPressed(self):
        self.stopAutoclose()
        username = self.sdk.database.getUserName(self.user)
        self.gui.launchKeyboardRequest("Recharge %s's account (\u20ac):"%username,
                                       float,self.rechargeAccount)
        
    def rechargeAccount(self,value):
        if value is not None :
            self.sdk.addRecharge(self.user,round(value,2))
        self.gui.changeWidgetSignal.emit('useraccount') 

        
        
        
        
        
        
        
    def renameButtonPressed(self):
        self.stopAutoclose()
        username = self.sdk.database.getUserName(self.user)
        self.gui.launchKeyboardRequest("Update %s's name:"%username,
                                       str,self.setName,initialValue=username,testFunction=self.checkName)
        
    def checkName(self,value):
        if value is not None :
            return value not in self.sdk.database.getUserNameList()
        else : 
            return False
            
    def setName(self,name):
        if name is not None :
            self.sdk.database.setUserName(self.user,name)
        self.gui.changeWidgetSignal.emit('useraccount') 
        
        
        
        
        
        
    def emailButtonPressed(self):
        self.stopAutoclose()
        username = self.sdk.database.getUserName(self.user)
        email = self.sdk.database.getUserEmail(self.user)
        if email is None :
            email = '@c2n.upsaclay.fr'
        self.gui.launchKeyboardRequest("Set %s's email address:"%username,
                                       str,self.setEmail,initialValue=email)

    def setEmail(self,value):
        if value is not None :
            if value == '' :
                self.sdk.database.setUserEmail(self.user,None)
            else :
                self.sdk.database.setUserEmail(self.user,value)
        self.gui.changeWidgetSignal.emit('useraccount')
        
        
        
        
        
        
    def consoButtonPressed(self): 
        self.sdk.addConso(self.user)
        self.gui.changeWidgetSignal.emit('useraccount')
    
    
    
    
    
    
    def tagButtonPressed(self):
        self.resetAutoclose()
        # Update database
        lastDetectionTime = self.sdk.var.getValue('rfid_time')
        if time.time() - lastDetectionTime <= 0.75 :
            tag = self.sdk.var.getValue('rfid_tag')
            if tag not in self.sdk.database.getUserTagList() :
                self.sdk.database.setUserTag(self.user,tag)
        else :
            self.sdk.database.setUserTag(self.user,None)
             
        # Update GUI
        self.gui.useraccount_tag_label.setText(str(self.sdk.database.getUserTag(self.user)))
        
    
    
    
    
    
    
    def setRedRechargeButton(self,state):
        if state is True :
            self.gui.useraccount_recharge_pushButton.setStyleSheet('background-color: red; font: bold 30px')
            self.gui.useraccount_balance_label.setStyleSheet('color: red; font: 40px')
        else :
            self.gui.useraccount_recharge_pushButton.setStyleSheet('font: bold 30px')
            self.gui.useraccount_balance_label.setStyleSheet('color: black; font: 40px')

    def setRedEmailButton(self,state):
        if state is True :
            self.gui.useraccount_email_pushButton.setStyleSheet('background-color: red; font: bold 30px')
        else :
            self.gui.useraccount_email_pushButton.setStyleSheet('font: bold 30px')
        
    def isToday(self,date):
        return date == self.getDateToday()
        
    def getDateToday(self):
        return dt.date.today()
        
    def previousDateButtonPressed(self):
        self.resetAutoclose()
        self.date -= dt.timedelta(days=1)
        self.updateDate()
        
    def nextDateButtonPressed(self):
        self.resetAutoclose()
        self.date += dt.timedelta(days=1)
        self.updateDate()
        
    def updateDate(self):
        
        # Activation buttons
        if self.isToday(self.date) is True : 
            self.gui.useraccount_nextDate_pushButton.setEnabled(False)
        else :
            self.gui.useraccount_nextDate_pushButton.setEnabled(True)
            
        # Display date    
        self.gui.useraccount_date_label.setText(self.date.strftime('%A\n%d/%m/%Y'))
        
        # Update details
        self.updateDetails()
        
        
    def updateDetails(self):
        
        # Reset
        self.gui.useraccount_details_textEdit.setHtml('<center>Please wait...</center>')
        
        # Starting new thread
        if 'detailsUpdater' in self.threads.keys() :
            self.gui.toThreadBin(self.threads['detailsUpdater']) 
        self.threads['detailsUpdater'] = DetailsUpdater(self)
        self.threads['detailsUpdater'].start()
        
        
    def enableAdminMode(self):
        self.gui.useraccount_tag_pushButton.setVisible(True)
        self.gui.useraccount_rename_pushButton.setVisible(True)
        self.gui.useraccount_tag_label.setVisible(True)
        self.gui.useraccount_tag_label.setText(str(self.sdk.database.getUserTag(self.user)))
           
    
    
    
    def donationDecreaseButtonPressed(self):
        self.resetAutoclose()
        currValue = self.sdk.database.getUserDonation(self.user)
        self.sdk.database.setUserDonation(self.user,currValue-0.01)
        self.updateDonation()
        
    def donationIncreaseButtonPressed(self):
        self.resetAutoclose()
        currValue = self.sdk.database.getUserDonation(self.user)
        self.sdk.database.setUserDonation(self.user,currValue+0.01)
        self.updateDonation()
        
    def updateDonation(self):
        value = self.sdk.database.getUserDonation(self.user)
        if value == 0 :
            self.gui.useraccount_donationDecrease_pushButton.setEnabled(False)
        else :
            self.gui.useraccount_donationDecrease_pushButton.setEnabled(True)
        self.gui.useraccount_donationValue_label.setText('%g \u20ac'%(value+0))
    


class Autoclose(QThread):

    def __init__(self,widget,delay):
        QThread.__init__(self)
        self.widget = widget
        self.gui = widget.gui 
        self.stopFlag = Event()
        self.delay = delay
    
    def run(self):
        t_autoclose = time.time()+self.delay
        while self.stopFlag.is_set() is False :
            remainingTime = round(t_autoclose - time.time())
            if remainingTime >= 0 :
                self.gui.useraccount_updateReturnTextSignal.emit('Return\n(%i)'%remainingTime)
                time.sleep(0.2)
            else :
                self.gui.useraccount_closePanelSignal.emit()
                self.stopFlag.set()




class BlinkingWarning(QThread):

    def __init__(self,window):
        QThread.__init__(self)
        self.gui = window.gui 
        self.stopFlag = Event()
        self.state = False
    
    def run(self):
        while self.stopFlag.is_set() is False :
            self.state = not self.state
            self.gui.useraccount_rechargeButtonBlinkingSignal.emit(self.state)
            time.sleep(0.5)
        self.gui.useraccount_rechargeButtonBlinkingSignal.emit(False)


class BlinkingEmail(QThread):

    def __init__(self,window):
        QThread.__init__(self)
        self.gui = window.gui 
        self.stopFlag = Event()
        self.state = False
    
    def run(self):
        while self.stopFlag.is_set() is False :
            self.state = not self.state
            self.gui.useraccount_emailButtonBlinkingSignal.emit(self.state)
            time.sleep(0.5)
        self.gui.useraccount_emailButtonBlinkingSignal.emit(False)
        

class DetailsUpdater(QThread):

    def __init__(self,widget):
        QThread.__init__(self)
        self.gui = widget.gui
        self.dtb = widget.sdk.database 
        self.widget = widget
        self.stopFlag = Event()
    
    def run(self):
        
        # Load Operations
        data = self.dtb.getUserOperationsByUserByDate(self.widget.user,self.widget.date.isoformat())        
        items = self.dtb.getItemDict()
        
        # Display operations
        if len(data) != 0 :
            data.loc[:,'datetime'] = pd.to_datetime(data.loc[:,'timestamp'])
            data.sort_values(by='datetime',inplace=True,ascending=False)
            data.reset_index(drop=True,inplace=True)
            opStr = ''
            lastHour = None
            for i in range(len(data)) :
                opStr += '<table width="100%" cellspacing="0" border="0"><tr class="address">'
                hour = data['datetime'][i].strftime('%H:%M')
                if hour != lastHour :
                    opStr += '<td width="30%">'+'%s</td>'%hour
                else :
                    opStr += '<td width="30%"></td>'
                lastHour = hour
                opStr += '<td width="40%">'+'  %s</td>'%items[data['item'][i]]
                if data['value'][i] >= 0 :
                    opStr += '<td width="30%" align="right">'+'+%g \u20ac</td>'%data['value'][i]
                else :
                    opStr += '<td width="30%" align="right">'+'%g \u20ac</td>'%data['value'][i]
                opStr += '</tr></table>' 
        else :
            opStr = '<center>Nothing to display</center>'
        
        if self.stopFlag.is_set() is False :
            self.gui.useraccount_refreshDetailsSignal.emit(opStr)
        