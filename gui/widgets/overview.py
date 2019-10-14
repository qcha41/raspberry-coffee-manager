# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 20:36:13 2018

@author: qchat
"""

import datetime as dt
from PyQt5.QtCore import QThread
from threading import Event
import pandas as pd

class OverviewPanel :

    def __init__(self,gui):
    
        self.gui=gui
        self.sdk=gui.sdk
        self.panel = self.gui.overview_panel
        self.gui.overview_return_pushButton.clicked.connect(self.returnButtonPressed)
        
    def returnButtonPressed(self):
        self.gui.changeWidgetSignal.emit('admin')
        
    def start(self):
    
        # SYSTEM BALANCE
        expenses_value = -self.sdk.database.getSystemOperationsValue()
        donations_system = self.sdk.database.getDonationsValue()
        recharges = self.sdk.database.getUsersRechargeValue()
        balance_system = recharges-expenses_value-donations_system
        self.gui.overview_sysBal_expenses_label.setText('%.2f \u20ac'%-expenses_value)
        self.gui.overview_sysBal_donations_label.setText('%.2f \u20ac'%-donations_system)
        self.gui.overview_sysBal_recharges_label.setText('%.2f \u20ac'%recharges)
        self.gui.overview_sysBal_balance_label.setText('%.2f \u20ac'%balance_system)
        
        # DONATION
        donations_users = self.sdk.database.getUsersDonationValue()
        donations_balance = donations_users - donations_system
        expensesCaps = self.sdk.database.getSystemOperationsCaps()
        self.gui.overview_donations_users_label.setText('%.2f \u20ac'%donations_users)
        self.gui.overview_donations_system_label.setText('%.2f \u20ac'%-donations_system)
        self.gui.overview_donations_tobedonated_label.setText('%.2f \u20ac'%donations_balance)
        
        
        # CAPS
        expenses_caps = self.sdk.database.getSystemOperationsCaps()
        conso_caps = self.sdk.database.getNbCapsUsed()
        conso_value = self.sdk.database.getValueCapsUsed()
        remaining_caps = expenses_caps - conso_caps
        remaining_value = expenses_value - conso_value
        caps_price = remaining_value/remaining_caps
        self.gui.overview_caps_expensesCaps_label.setText('%i'%expenses_caps)
        self.gui.overview_caps_expensesValue_label.setText('%.2f \u20ac'%-expenses_value)
        self.gui.overview_caps_consoCaps_label.setText('%i'%-conso_caps)
        self.gui.overview_caps_consoValue_label.setText('%.2f \u20ac'%conso_value)
        self.gui.overview_caps_remainingCaps_label.setText('%i'%remaining_caps)
        self.gui.overview_caps_remainingValue_label.setText('%.2f \u20ac'%-remaining_value)
        self.gui.overview_caps_capsPrice_label.setText('%.2f \u20ac'%caps_price)
        
        
        
    def stop(self):
        pass
        
    
        