# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 20:36:13 2018

@author: qchat
"""



class AdminPanel :

    def __init__(self,gui):
    
        self.gui=gui
        self.sdk=gui.sdk
        self.panel = self.gui.admin_panel
        
        self.userList = None
        self.userSelected = None
        
        self.gui.admin_return_pushButton.clicked.connect(self.returnPushButtonClicked)
        self.gui.admin_nextUser_pushButton.clicked.connect(self.nextUser)
        self.gui.admin_previousUser_pushButton.clicked.connect(self.previousUser)
        self.gui.admin_user_pushButton.clicked.connect(self.userButtonClicked)
        self.gui.admin_allUsers_pushButton.clicked.connect(self.allUsersButtonClicked)
        self.gui.admin_email_checkBox.stateChanged.connect(self.emailCheckboxStateChanged)
        self.gui.admin_restart_pushButton.clicked.connect(self.restartButtonClicked)
        self.gui.admin_shutdown_pushButton.clicked.connect(self.shutdownButtonClicked)
        self.gui.admin_overview_pushButton.clicked.connect(self.overviewButtonClicked)
        self.gui.admin_expenses_pushButton.clicked.connect(self.expensesButtonClicked)
        self.gui.admin_donations_pushButton.clicked.connect(self.donationsButtonClicked)
        
        # Close button
        self.gui.admin_close_pushButton.clicked.connect(self.closeApp)
        
    def closeApp(self):
        self.sdk.system.close()
        
    def start(self):        
        
        self.userList = sorted(self.sdk.database.getUserNameList())
        if len(self.userList)>0 :
            self.gui.admin_previousUser_pushButton.setEnabled(True)
            self.gui.admin_nextUser_pushButton.setEnabled(True)
            self.gui.admin_user_pushButton.setEnabled(True)
            self.userSelected = self.userList[0]
            self.updateUserButton()
        else :
            self.gui.admin_previousUser_pushButton.setEnabled(False)
            self.gui.admin_nextUser_pushButton.setEnabled(False)
            self.gui.admin_user_pushButton.setEnabled(False)
        
        self.gui.admin_email_checkBox.setChecked(self.sdk.var.getValue('email'))

        
    def stop(self):
        pass 
    
    
    
    
    def shutdownButtonClicked(self):
        self.sdk.system.shutdown()
        
    def restartButtonClicked(self):
        self.sdk.system.restart()
        
        
        
        
        
    def returnPushButtonClicked(self):
        self.gui.changeWidgetSignal.emit('accueil')
        
        
        
        
        
    def previousUser(self):
        idx = self.userList.index(self.userSelected)
        self.userSelected = self.userList[(idx - 1) % len(self.userList)]
        self.updateUserButton()
            
    def nextUser(self):
        idx = self.userList.index(self.userSelected)
        self.userSelected = self.userList[(idx + 1) % len(self.userList)]
        self.updateUserButton()
        
    def updateUserButton(self):
        self.gui.admin_user_pushButton.setText('USER\n(%s)'%self.userSelected)

    def userButtonClicked(self):
        user = self.sdk.database.getUserByName(self.userSelected)
        self.sdk.var.setValue('activeUser',user)
        self.gui.changeWidgetSignal.emit('useraccount')
        
        
        
        
        

        
    def allUsersButtonClicked(self):
        self.gui.changeWidgetSignal.emit('operations')
        
    def overviewButtonClicked(self):
        self.gui.changeWidgetSignal.emit('overview')
        
    def expensesButtonClicked(self):
        self.gui.changeWidgetSignal.emit('expenses')
        
    def donationsButtonClicked(self):
        self.gui.changeWidgetSignal.emit('donations')
        
    def emailCheckboxStateChanged(self):
        state = self.gui.admin_email_checkBox.isChecked()
        self.sdk.var.setValue('email',state)
        