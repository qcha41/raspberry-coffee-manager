# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 20:36:13 2018

@author: qchat
"""

import datetime as dt
from PyQt5.QtCore import QThread, pyqtSignal
from threading import Event
import pandas as pd

class OperationsPanel :

    def __init__(self,gui):
    
        self.gui=gui
        self.sdk=gui.sdk
        self.panel = self.gui.operations_panel
        
        self.threads = {}
        
        self.gui.operations_caps_checkBox.setChecked(True)
        self.gui.operations_donation_checkBox.setChecked(True)
        self.gui.operations_recharge_checkBox.setChecked(True)
        
        self.gui.operations_return_pushButton.clicked.connect(self.returnButtonClicked)
        self.gui.operations_previousDate_pushButton.clicked.connect(self.previousDateButtonPressed)
        self.gui.operations_nextDate_pushButton.clicked.connect(self.nextDateButtonPressed)
        self.gui.operations_refreshDetailsSignal.connect(self.gui.operations_details_textEdit.setHtml)
        self.gui.operations_caps_checkBox.stateChanged.connect(self.updateInfos)
        self.gui.operations_donation_checkBox.stateChanged.connect(self.updateInfos)
        self.gui.operations_recharge_checkBox.stateChanged.connect(self.updateInfos)
        
        self.dateSelected = None
        
    def start(self):
        self.dateSelected = self.getDateToday()
        self.updateInfos()
        
        
        
    def stop(self):
        self.gui.keyPressedFunction = None
        for name in self.threads.keys() :
            self.gui.toThreadBin(self.threads[name])
        self.threads = {}
        
     # DATE UPDATE
     

        

    def setEnabledDateButton(self,value):
        self.gui.operations_previousDate_pushButton.setEnabled(value)
        if value is True and self.isDateSelectedToday() is False : 
            self.gui.operations_nextDate_pushButton.setEnabled(True)
        else :
            self.gui.operations_nextDate_pushButton.setEnabled(False)
        
    def isDateSelectedToday(self):
        return self.dateSelected == self.getDateToday()
        
    def getDateToday(self):
        return dt.date.today()
        
    def previousDateButtonPressed(self):
        self.dateSelected -= dt.timedelta(days=1)
        self.updateInfos()
        
    def nextDateButtonPressed(self):
        self.dateSelected += dt.timedelta(days=1)
        self.updateInfos()
        
    def updateInfos(self):
    
        # Desactivation interface
        if self.isDateSelectedToday() is True : 
            self.gui.operations_nextDate_pushButton.setEnabled(False)
        else :
            self.gui.operations_nextDate_pushButton.setEnabled(True)
            
        # Display date    
        self.gui.operations_date_label.setText(self.dateSelected.strftime('%A\n%d/%m/%Y'))
        
        # Reset details
        self.updateDetails('<center>Please wait...</center>','Nb conso\n')
        
        # Suppression current thread
        if 'detailsUpdater' in self.threads.keys() :
            self.gui.toThreadBin(self.threads['detailsUpdater'])
            
        # Starting new thread
        self.threads['detailsUpdater'] = DetailsUpdater(self)
        self.threads['detailsUpdater'].start()
        
        

        
        
        
       
    def returnButtonClicked(self):
        self.gui.changeWidgetSignal.emit('admin')           
        
    def updateDetails(self,opStr,nbConsoStr):
        self.gui.operations_refreshDetailsSignal.emit(opStr)
        self.gui.operations_nbconso_label.setText(nbConsoStr)
        
        


class DetailsUpdater(QThread):

    def __init__(self,widget):
        QThread.__init__(self)
        self.gui = widget.gui
        self.dtb = widget.sdk.database 
        self.widget = widget
        self.stopFlag = Event()
    
    def run(self):
        
        # Load Operations
        data = self.dtb.getUserOperationsByDate(self.widget.dateSelected.isoformat())        
        items = self.dtb.getItemDict()
        users = self.dtb.getUserDict()
        capsItem = self.dtb.getItemByName('Caps')
        donationItem = self.dtb.getItemByName('Donation')
        rechargeItem = self.dtb.getItemByName('Recharge')
        
        
        # Display operations
        if len(data) != 0 :      
        
            nbcaps = len(data.query('item==%i'%capsItem))
            
            if self.gui.operations_caps_checkBox.isChecked() is False :
                data = data[data.item != capsItem]
            if self.gui.operations_donation_checkBox.isChecked() is False :
                data = data[data.item != donationItem]
            if self.gui.operations_recharge_checkBox.isChecked() is False :
                data = data[data.item != rechargeItem]
                
            data.loc[:,'datetime'] = pd.to_datetime(data.loc[:,'timestamp'])
            data.sort_values(by='datetime',inplace=True,ascending=False)
            data.reset_index(drop=True,inplace=True)  
            
            opStr = ''
            lastHour = None
            for i in range(len(data)) :
                opStr += '<table width="100%" cellspacing="0" border="0"><tr class="address">'
                hour = data['datetime'][i].strftime('%H:%M')
                if hour != lastHour :
                    opStr += '<td width="20%">'+'%s</td>'%hour
                else :
                    opStr += '<td width="20%"></td>'
                lastHour = hour
                opStr += '<td width="30%" align="center">'+'%s</td>'%users[data['user'][i]]
                opStr += '<td width="30%" align="center">'+'%s</td>'%items[data['item'][i]]
                opStr += '<td width="20%" align="right">'+'%g \u20ac</td>'%data['value'][i]
                opStr += '</tr></table>'
            
        else :
            opStr = '<center>Nothing to display</center>'
            nbcaps = 0
        
        if self.stopFlag.is_set() is False :
            self.gui.operations_updateDetailsSignal.emit(opStr,'Nb caps\n%i'%nbcaps)

        
        