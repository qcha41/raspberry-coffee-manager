# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 20:36:13 2018

@author: qchat
"""

import datetime as dt
from PyQt5.QtCore import QThread, pyqtSignal
from threading import Event
import pandas as pd

class ExpensesPanel :

    def __init__(self,gui):
    
        self.gui=gui
        self.sdk=gui.sdk
        self.panel = self.gui.expenses_panel
        
        self.threads = {}
        
        self.gui.expenses_return_pushButton.clicked.connect(self.returnButtonPressed)
        
        self.gui.expenses_add_pushButton.clicked.connect(self.addExpense)
        self.gui.expenses_description_pushButton.clicked.connect(self.description_clicked)
        self.gui.expenses_caps_pushButton.clicked.connect(self.caps_clicked)
        self.gui.expenses_cost_pushButton.clicked.connect(self.cost_clicked)
        
        self.gui.expenses_description_pushButton.setStyleSheet('background-color: white;')
        self.gui.expenses_caps_pushButton.setStyleSheet('background-color: white;')
        self.gui.expenses_cost_pushButton.setStyleSheet('background-color: white;')
        
    def returnButtonPressed(self):
        self.gui.changeWidgetSignal.emit('admin')

        
    def start(self):

        self.resetFields()
        self.updateInfos()        
        
        
        
    def stop(self):
        self.gui.keyPressedFunction = None
        for name in self.threads.keys() :
            self.gui.toThreadBin(self.threads[name])
        self.threads = {}
        

    def updateInfos(self):

        # Reset details
        self.updateDetails('<center>Please wait...</center>')
        
        # Suppression current thread
        if 'detailsUpdater' in self.threads.keys() :
            self.gui.toThreadBin(self.threads['detailsUpdater'])
            
        # Starting new thread
        self.threads['detailsUpdater'] = DetailsUpdater(self)
        self.threads['detailsUpdater'].start()
        
        

    def addExpense(self):
        description = self.gui.expenses_description_pushButton.text()
        caps = self.gui.expenses_caps_pushButton.text()
        cost = self.gui.expenses_cost_pushButton.text()
        
        if description != '' :
            if caps != '' :
                if cost != '' :
                    self.sdk.newExpense(description,int(caps),-float(cost))
                    self.resetFields()
                    self.updateInfos()
    
    
    def resetFields(self):
        self.gui.expenses_description_pushButton.setText('')
        self.gui.expenses_caps_pushButton.setText('')
        self.gui.expenses_cost_pushButton.setText('')
    
    def description_clicked(self):
        currValue = self.gui.expenses_description_pushButton.text()
        self.gui.launchKeyboardRequest("Enter expense description:",
                                       str,self.updateDescription,initialValue = currValue)
        
    def updateDescription(self,value):
        if value is not None :
            self.gui.expenses_description_pushButton.setText(str(value))
        else :
            self.gui.expenses_description_pushButton.setText('')
        
        
        
        
    def caps_clicked(self):
        currValue = self.gui.expenses_caps_pushButton.text()
        self.gui.launchKeyboardRequest("Enter expense caps added:",
                                       int,self.updateCaps,initialValue = currValue)
        
    def updateCaps(self,value):
        if value is not None :
            self.gui.expenses_caps_pushButton.setText(str(value))
        else :
            self.gui.expenses_caps_pushButton.setText('')
        
        
        
        
    def cost_clicked(self):
        currValue = self.gui.expenses_cost_pushButton.text()
        self.gui.launchKeyboardRequest("Enter expense cost :",
                                       float,self.updateCost,initialValue = currValue)
        
    def updateCost(self,value):
        if value is not None :
            self.gui.expenses_cost_pushButton.setText(str(value))
        else :
            self.gui.expenses_cost_pushButton.setText('')
       
        
        
        
    def returnButtonClicked(self):
        self.gui.changeWidgetSignal.emit('admin')           
        
    def updateDetails(self,opStr):
        self.gui.expenses_details_textEdit.setHtml(opStr)
        
        
        
        


class DetailsUpdater(QThread):

    def __init__(self,widget):
        QThread.__init__(self)
        self.gui = widget.gui
        self.dtb = widget.sdk.database 
        self.widget = widget
        self.stopFlag = Event()
    
    def run(self):
        
        # Load Operations
        data = self.dtb.getSystemOperations()
        
        
        # Display operations
        if len(data) != 0 :      
                
            data.loc[:,'datetime'] = pd.to_datetime(data.loc[:,'timestamp'])
            data.sort_values(by='datetime',inplace=True,ascending=False)
            data.reset_index(drop=True,inplace=True)  
            data = data.loc[:20]
            
            opStr = ''
            opStr += '<table width="100%" cellspacing="0" border="0"><tr class="address">'
            opStr += '<td width="20%" align="center">Date</td>'
            opStr += '<td width="40%" align="center">Description</td>'
            opStr += '<td width="20%" align="center">Caps</td>'
            opStr += '<td width="20%" align="center">Value</td>'
            opStr += '</tr></table>'
            for i in range(len(data)) :
                opStr += '<table width="100%" cellspacing="0" border="0"><tr class="address">'
                opStr += '<td width="20%" align="center">'+'%s</td>'%data['datetime'][i].date().isoformat()
                opStr += '<td width="40%" align="center">'+'%s</td>'%data['description'][i]
                opStr += '<td width="20%" align="center">'+'%i</td>'%data['caps'][i]
                opStr += '<td width="20%" align="center">'+'%g \u20ac</td>'%data['value'][i]
                opStr += '</tr></table>'
            
        else :
            opStr = '<center>Nothing to display</center>'

        
        if self.stopFlag.is_set() is False :
            self.gui.expenses_updateDetailsSignal.emit(opStr)

        
        