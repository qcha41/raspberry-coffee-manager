# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 20:37:52 2020

@author: qchat
"""

from ...api.database import system
from ...api import system as system_pi
from ...api import email
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QHBoxLayout, QCheckBox, QWidget
from PyQt5.QtCore import Qt

class AdminPanel():
    
    def __init__(self,gui):
        
        self.gui = gui
        
        # Connect signals
        self.gui.admin_close_pushButton.clicked.connect(self.gui.close)
        self.gui.admin_shutdown_pushButton.clicked.connect(system_pi.shutdown)
        self.gui.admin_restart_pushButton.clicked.connect(system_pi.reboot)
        self.gui.admin_email_checkBox.stateChanged.connect(self.switch_email_state)
        self.gui.admin_email_checkBox.stateChanged.connect(self.gui.countdown.start)
        self.gui.admin_return_pushButton.clicked.connect(self.return_pressed)
        self.gui.admin_display_comboBox.activated.connect(self.show_details)
        self.gui.admin_display_comboBox.activated.connect(self.gui.countdown.start)
        self.gui.admin_details_table.cellClicked.connect(self.gui.countdown.start)
        self.gui.admin_addOperation_comboBox.activated.connect(self.do_operation)
        self.gui.admin_testemail_pushButton.clicked.connect(email.test)
        self.gui.admin_testemail_pushButton.clicked.connect(self.gui.countdown.start)
        
        # Configure tablew widget
        self.gui.admin_details_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.gui.admin_details_table.verticalHeader().setVisible(False)
        self.gui.admin_details_table.cellClicked.connect(self.cell_clicked)
        self.base_item = QTableWidgetItem()
        self.base_item.setTextAlignment(Qt.AlignCenter)
        self.check_box_dict = None

        # Return countdown
        self.callback_countdown_update = lambda x : self.gui.admin_return_pushButton.setText(f'Return\n({x})')
        self.callback_countdown_end = self.return_pressed
        
        
    def start(self):
        
        ''' Initialize panel '''
        
        # Email checkBox
        self.gui.admin_email_checkBox.setChecked(self.gui.send_email)
        
        # Admin balance
        self.gui.admin_balance_label.setText(str(system.get_balance())+' \u20ac')
        
        # Users
        nb_users = system.get_nb_users()
        nb_users_active = system.get_nb_users(only_active=True)
        self.gui.admin_nbusers_label.setText(f'{nb_users} users ({nb_users_active} active)')
        
        # Display
        self.show_details(self.gui.admin_display_comboBox.currentText())
        
        # Return button
        self.gui.countdown.start()
        
    
    
    def stop(self):
        
        ''' Uninitialize panel '''
        
        pass
    
    
    def do_operation(self,operation_index):
        
        operation_name = self.gui.admin_addOperation_comboBox.currentText()  
        if operation_name == 'Caps purchase' : self.start_caps_purchase_operation_part1()
        elif operation_name == 'Missing caps' : self.start_missing_caps_operation()
        elif operation_name == 'Supplies purchase' : self.start_supplies_purchase_operation()
        elif operation_name == 'System donation' : self.start_system_donation_operation()
            
            
    def start_caps_purchase_operation_part1(self):
        
        keyboard = self.gui.widgets['keyboard']
        keyboard.return_panel = 'admin'
        keyboard.callback_end = self.start_caps_purchase_operation_part2
        keyboard.text_function = lambda value : f"{value} caps bought...\n"
        keyboard.requested_type = int
        keyboard.test_function = lambda x : x != 0
        keyboard.auto_return = False
        self.gui.switch_panel_signal.emit('keyboard') 
        
        
    def start_caps_purchase_operation_part2(self,qty):
        
        keyboard = self.gui.widgets['keyboard']
        keyboard.stop()        
        keyboard.return_panel = 'admin'
        keyboard.callback_end = lambda price, qty=qty : system.add_caps_purchase(qty,price)
        keyboard.text_function = lambda value : f"{qty} caps bought...\n... for {value} \u20ac"
        keyboard.requested_type = float
        keyboard.start()
        
        
    def start_supplies_purchase_operation(self):
        
        keyboard = self.gui.widgets['keyboard']
        keyboard.return_panel = 'admin'
        keyboard.callback_end = system.add_supplies_purchase
        keyboard.text_function = lambda value : f"Supplies bought for {value} \u20ac"
        keyboard.requested_type = float
        keyboard.test_function = lambda x : x != 0
        self.gui.switch_panel_signal.emit('keyboard') 
        
    def start_missing_caps_operation(self):
        
        keyboard = self.gui.widgets['keyboard']
        keyboard.return_panel = 'admin'
        keyboard.callback_end = system.remove_missing_caps
        keyboard.text_function = lambda value : f"Declare {value} missing caps"
        keyboard.requested_type = int
        keyboard.test_function = lambda x : x != 0
        self.gui.switch_panel_signal.emit('keyboard') 
        
    def start_system_donation_operation(self):
        
        keyboard = self.gui.widgets['keyboard']
        keyboard.return_panel = 'admin'
        keyboard.callback_end = system.add_charity_donation
        keyboard.text_function = lambda value : f"Declare {value} \u20ac to charity"
        keyboard.requested_type = float
        keyboard.test_function = lambda x : x != 0
        self.gui.switch_panel_signal.emit('keyboard') 
        
        
    def add_base_item(self, row, column, text):
        
        widget = self.base_item.clone()
        widget.setText(text)
        self.gui.admin_details_table.setItem(row, column, widget)
    
    def show_details(self,display_id):
        
        self.check_box_dict = {}
        
        ''' Update the details of the table name selected '''
        
        self.gui.admin_details_table.clear()
        self.gui.admin_details_table.setColumnCount(0)
        self.gui.admin_details_table.setRowCount(0)
        self.gui.admin_sumup_label.setText('')
        fnt = self.gui.admin_details_table.font()
        fnt.setPointSize(11)
        self.gui.admin_details_table.setFont(fnt)

        display_name = self.gui.admin_display_comboBox.currentText()        
        if display_name == 'Accounts':
            
            # Load operations
            operations = system.get_account_operations()
            operations.sort_values(by='timestamp',inplace=True,ascending=False)

            # Configure table widget
            self.gui.admin_details_table.setColumnCount(5)
            self.gui.admin_details_table.setRowCount(50)
            self.gui.admin_details_table.setHorizontalHeaderLabels(['Timestamp','User','Label','Value','Checked'])

            # Fill table widget
            for i in range(50) :
                self.add_base_item(i, 0, str(operations.iloc[i].timestamp))
                self.add_base_item(i, 1, str(operations.iloc[i].user))
                self.add_base_item(i, 2, str(operations.iloc[i].label))
                self.add_base_item(i, 3, str(operations.iloc[i].value))
                
                widget = QWidget()
                checkbox = QCheckBox()
                checkbox.setChecked(bool(operations.iloc[i].checked))
                checkbox.stateChanged.connect(lambda state, ID=int(operations.iloc[i].id), checkbox=checkbox : self.checkbox_state_changed(ID,state,checkbox))
                self.check_box_dict[i] = checkbox
                hboxlayout = QHBoxLayout(widget)
                hboxlayout.addWidget(checkbox)
                hboxlayout.setAlignment(Qt.AlignCenter)
                hboxlayout.setContentsMargins(0,0,0,0)
                widget.setLayout(hboxlayout)
                self.gui.admin_details_table.setCellWidget(i,4,widget)
            
            # Sumup
            sumup = ''
            sumup += f'Recharges\n{system.get_total_recharges()} \u20ac\n\n'
            sumup += f'Shares\n{system.get_total_shares()} \u20ac\n\n'
            self.gui.admin_sumup_label.setText(sumup)
                
        elif display_name == 'Caps':
            
            # Load operations
            operations = system.get_system_caps_operations()
            operations.sort_values(by='timestamp',inplace=True,ascending=False)

            # Configure table widget
            self.gui.admin_details_table.setColumnCount(4)
            self.gui.admin_details_table.setRowCount(len(operations))
            self.gui.admin_details_table.setHorizontalHeaderLabels(['Timestamp','Label','Qty','Value'])
            
            # Fill table widget
            for i in range(len(operations)) :
                self.add_base_item(i, 0, str(operations.iloc[i].timestamp))
                self.add_base_item(i, 1, str(operations.iloc[i].label))
                self.add_base_item(i, 2, str(operations.iloc[i].qty))
                self.add_base_item(i, 3, str(operations.iloc[i].value))
            
            # Sumup
            sumup = ''
            sumup += f'System: {system.get_caps_remaining_system()}\n{system.get_caps_balance_system()} \u20ac\n\n'
            sumup += f'Users: {system.get_caps_remaining_users()}\n{system.get_caps_balance_users()} \u20ac\n\n'
            sumup += f'Remaining: {system.get_caps_remaining()}\n{system.get_caps_balance()} \u20ac\n\n'
            sumup += f'Caps price\n{system.get_caps_price()} \u20ac'
            self.gui.admin_sumup_label.setText(sumup)
                
        elif display_name == 'Donations':
            
            # Load operations
            operations = system.get_system_donation_operations()
            operations.sort_values(by='timestamp',inplace=True,ascending=False)

            # Configure table widget
            self.gui.admin_details_table.setColumnCount(3)
            self.gui.admin_details_table.setRowCount(len(operations))
            self.gui.admin_details_table.setHorizontalHeaderLabels(['Timestamp','Label','Value'])
            
            # Fill table widget
            for i in range(len(operations)) :
                self.add_base_item(i, 0, str(operations.iloc[i].timestamp))
                self.add_base_item(i, 1, str(operations.iloc[i].label))
                self.add_base_item(i, 2, str(operations.iloc[i].value))
            
            # Sumup
            sumup = ''
            sumup += f'User donations\n{system.get_users_donation_balance()} \u20ac\n\n'
            sumup += f'System donations\n{system.get_system_donation_balance()} \u20ac\n\n'
            sumup += f'To be donated\n{system.get_donation_balance()} \u20ac'
            self.gui.admin_sumup_label.setText(sumup)
                
            
            
    def cell_clicked(self,row,col):
        
        if self.gui.admin_display_comboBox.currentText() == 'Accounts' :
            if col == 4 : 
                state = self.check_box_dict[row].isChecked()
                self.check_box_dict[row].setChecked(not state)
            
        
    def checkbox_state_changed(self,ID,state,checkbox):
        
        ''' Change checked state in database and update GUI '''
        
        state = bool(state/2)
        system.set_account_operation_checked(ID,state)
        checkbox.setChecked(system.is_account_operation_checked(ID))
        self.gui.countdown.start()
        
        
    
    def switch_email_state(self):
        
        ''' Enable/Disable email sending '''
        
        state = self.gui.admin_email_checkBox.isChecked()
        self.gui.send_email = state
        
    
    
    # Return
    # =========================================================================
    
    def return_pressed(self):
        
        ''' Return to main panel '''
        
        self.gui.switch_panel_signal.emit('main') 