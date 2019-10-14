# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 20:36:13 2018

@author: qchat
"""

import pandas as pd

class DonationsPanel :

    def __init__(self,gui):
    
        self.gui=gui
        self.sdk=gui.sdk   
        self.panel = self.gui.donations_panel
        self.gui.donations_return_pushButton.clicked.connect(self.returnButtonClicked)
        self.gui.donations_add_pushButton.clicked.connect(self.addButtonClicked)
        
    def start(self):
        self.updateInfos()
        
        
    def stop(self):
        pass
    
    
    def addButtonClicked(self):
        self.gui.launchKeyboardRequest("Enter donation:",
                                       float,self.addDonation)
        
    def addDonation(self,value):
        if value is not None and value != 0:
            self.sdk.database.newDonation(value)
            self.updateInfos()
        
    def updateInfos(self):
    
        # Load Operations
        data = self.sdk.database.getDonations()      
        
        # Display operations
        if len(data) != 0 :      
                    
            data.loc[:,'datetime'] = pd.to_datetime(data.loc[:,'timestamp'])
            data.sort_values(by='datetime',inplace=True,ascending=False)
            data.reset_index(drop=True,inplace=True)  
            
            opStr = ''
            for i in range(len(data)) :
                opStr += '<table width="100%" cellspacing="0" border="0"><tr class="address">'
                opStr += '<td width="50%" align="center">'+'%s</td>'%data['timestamp'][i]
                opStr += '<td width="50%" align="center">'+'%s</td>'%data['value'][i]
                opStr += '</tr></table>'
            
        else :
            opStr = '<center>Nothing to display</center>'

        self.gui.donations_details_textEdit.setHtml(opStr)
        
        
        
       
    def returnButtonClicked(self):
        self.gui.changeWidgetSignal.emit('admin')           
        
    def updateDetails(self,opStr,nbConsoStr):
        self.gui.donations_refreshDetailsSignal.emit(opStr)
        self.gui.operations_nbconso_label.setText(nbConsoStr)
        
        