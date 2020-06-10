# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 12:52:30 2020

@author: qchat
"""

import datetime
import pandas as pd

from ...api import email
from ...api.devices import devices


class AccountPanel():
    
    def __init__(self,gui):
        
        self.gui = gui
        self.user = None
        
        # Connect signal
        self.gui.account_previousDate_pushButton.clicked.connect(self.decrease_date)
        self.gui.account_previousDate_pushButton.clicked.connect(self.gui.countdown.start)
        self.gui.account_nextDate_pushButton.clicked.connect(self.increase_date)
        self.gui.account_nextDate_pushButton.clicked.connect(self.gui.countdown.start)
        self.gui.account_conso_pushButton.clicked.connect(self.add_conso)
        self.gui.account_conso_pushButton.clicked.connect(self.gui.countdown.start)
        self.gui.account_return_pushButton.clicked.connect(self.return_pressed)
        self.gui.account_configure_pushButton.clicked.connect(self.configure_pressed)
        self.gui.account_statistics_pushButton.clicked.connect(self.stats_pressed)
        self.gui.account_recharge_pushButton.clicked.connect(self.recharge_button_pressed)
        self.gui.account_manualdonation_pushButton.clicked.connect(self.manualdonation_button_pressed)
        
        # Return countdown
        self.callback_countdown_update = lambda x : self.gui.account_return_pushButton.setText(f'Return\n({x})')
        self.callback_countdown_end = self.return_pressed
        
        
    
    def start(self):
        
        ''' Initialize panel '''
        
        self.user = self.gui.current_user
        
        # Display name
        self.gui.account_username_label.setText(f'{self.user.get_name()}')
        
        # Display balance
        self.display_balance()
        
        # Initialize details
        self.set_date(datetime.date.today())
        
        # Enable or disable conso recharge buttons
        self.gui.account_conso_pushButton.setEnabled(self.user.is_active())
        self.gui.account_recharge_pushButton.setEnabled(self.user.is_active())
        self.gui.account_manualdonation_pushButton.setEnabled(self.user.is_active())
        
        # Return button
        self.gui.countdown.start()
        
        
        
    def stop(self):
        
        ''' Uninitialize panel '''
        
        devices.led.set_scenario('idle')
    
    
    # Add conso / conso / manual donation
    # =========================================================================
    
    def add_conso(self):
        
        ''' Add a conso in this account '''
        
        if self.user.is_active() :
            self.user.add_conso()
            devices.buzzer.short_beep()
            balance = self.user.get_balance()
            if balance<0 and self.gui.send_email is True :
                email.notify_negative_balance(self.user.get_email(),self.user.get_name(),balance)
            self.display_balance()
            self.set_date(datetime.date.today())
        

    def recharge_button_pressed(self):    
        
        ''' Start a keyboard request to add shares '''
        
        keyboard = self.gui.widgets['keyboard']
        keyboard.return_panel = 'account'
        keyboard.callback_end = self.user.add_recharge
        keyboard.text_function = lambda value : f"Recharge {value} \u20ac"
        keyboard.requested_type = float
        keyboard.test_function = lambda x : x != 0
        self.gui.switch_panel_signal.emit('keyboard') 
        
    
    def manualdonation_button_pressed(self):    
        
        ''' Start a keyboard request to add a manual donation '''
        
        keyboard = self.gui.widgets['keyboard']
        keyboard.return_panel = 'account'
        keyboard.callback_end = self.user.add_manual_donation
        keyboard.text_function = lambda value : f"Donate manually {value} \u20ac"
        keyboard.requested_type = float
        keyboard.test_function = lambda x : x > 0
        self.gui.switch_panel_signal.emit('keyboard') 
        
        
        
    # Return, configure, stats buttons
    # =========================================================================
    
    def return_pressed(self):
        
        ''' Return to main panel '''
        
        self.gui.switch_panel_signal.emit('main') 
        

    
    def configure_pressed(self):
        
        ''' Open account setup panel '''
        
        self.gui.switch_panel_signal.emit('account_setup')
        
        
    def stats_pressed(self):
        
        ''' Open stats panel '''
        
        self.gui.switch_panel_signal.emit('stats')
        
    
    # Date selection
    # =========================================================================
    
    def increase_date(self):
        
        ''' Increase current day by one day if not in the future'''
        
        if self.date + datetime.timedelta(days=1) <= datetime.date.today() :
            self.set_date( self.date + datetime.timedelta(days=1) )
        
        
    def decrease_date(self):
        
        ''' Decrease current day by one day '''
        
        self.set_date( self.date - datetime.timedelta(days=1) )
        
        
    def set_date(self,date):
        
        ''' Set given date for details '''
        
        self.date = date
        self.gui.account_date_label.setText(self.date.strftime('%A\n%d/%m/%Y'))
        self.update_details()



    # Details
    # =========================================================================

    def update_details(self):
        
        ''' Load and display user details for the selected date '''
        
        # Load Operations
        data = self.user.get_operations_by_date(self.date.year,self.date.month,self.date.day)
        
        # Display operations
        if len(data) != 0 :
            data.loc[:,'datetime'] = pd.to_datetime(data.loc[:,'timestamp'])
            data.sort_values(by='datetime',inplace=True,ascending=False)
            data.reset_index(drop=True,inplace=True)
            
            opStr = ''
            lastHour = None
            for i in range(len(data)) :
                
                # Hour column
                opStr += '<table width="100%" cellspacing="0" border="0"><tr class="address">'
                hour = data['datetime'][i].strftime('%H:%M')
                if hour != lastHour :
                    opStr += f'<td width="30%">{hour}</td>'
                else :
                    opStr += '<td width="30%"></td>'
                lastHour = hour
                
                # Label
                opStr += f'<td width="40%" align="center">  {data["label"][i]}</td>'
                
                # Value
                if data['value'][i] >= 0 :
                    opStr += f'<td width="30%" align="right">+{data["value"][i]} \u20ac</td>'
                else :
                    opStr += f'<td width="30%" align="right">{data["value"][i]} \u20ac</td>'
                opStr += '</tr></table>' 
        else :
            opStr = '<center>Nothing to display</center>'
    
        self.gui.account_details_textEdit.setHtml(opStr)
    



    
    # Balance
    # =========================================================================
    
    def display_balance(self):
        
        ''' Load and display current user balance '''
        
        balance = self.user.get_balance()
        
        if balance > 0 :
            self.gui.account_balance_label.setStyleSheet('color: green; font: bold 30pt')
            text = f'+{balance} \u20ac'
            devices.led.set_scenario('fixed_green')
        elif balance < 0 :
            self.gui.account_balance_label.setStyleSheet('color: red; font: bold 30pt')
            text = f'{balance} \u20ac'
            devices.led.set_scenario('low_blinking_orange')
        else : 
            self.gui.account_balance_label.setStyleSheet('color: black; font: bold 30pt')
            text = f'{balance} \u20ac'
            devices.led.set_scenario('high_blinking_red')
            
        self.gui.account_balance_label.setText(text)
        
        
        
        