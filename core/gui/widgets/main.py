# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 22:17:14 2020

@author: qchat
"""

from PyQt5.QtGui import QPixmap
import os

from ...api import config
from ...api.database import system
from ...api.database.users import User

class MainPanel():
    
    def __init__(self,gui):
        
        self.gui = gui
        
        # Connect signals
        self.gui.main_disable_pushButton.clicked.connect(self.switch_autoconso_state)
        self.gui.main_admin_pushButton.clicked.connect(self.admin_button_pressed)
        self.gui.main_newuser_pushButton.clicked.connect(lambda : self.gui.switch_panel_signal.emit('new_user'))
        self.gui.update_system_infos_signal.connect(self.update_system_infos_signal)
        
        # System name
        self.gui.main_systemname_label.setText(config['GENERAL']['system_name'])
        
        # RFID logo
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'rfid_logo.png')
        self.pixmap = QPixmap(image_path).scaledToHeight(self.gui.main_rfidImage_label.frameGeometry().height())
        self.gui.main_rfidImage_label.setPixmap(self.pixmap)
        
        # User selector
        self.gui.main_previousUser_pushButton.clicked.connect(self.previous_user)
        self.gui.main_nextUser_pushButton.clicked.connect(self.next_user)
        self.gui.main_user_pushButton.clicked.connect(self.user_button_clicked)
        self.user_dict = None
        self.user_id_list = None
        self.user_id_list_curr_pos = None
        
        # Countdown
        self.callback_countdown_update = lambda x : self.gui.main_disable_pushButton.setText(f'Enable ({x})')
        self.callback_countdown_end = lambda : self.set_autoconso_state(True)
        
        # Auto conso
        self.autoconso_state = True
        self.set_autoconso_state(self.autoconso_state)
        
        
        
    def start(self):
        
        ''' Initialize panel '''
        
        # Connect signals
        self.gui.rfid_tag_detected_signal.connect(self.tag_detected_callback)
        
        # Update caps price
        self.gui.main_capsprice_label.setText(str(system.get_caps_price())+' \u20ac')
        
        # Reset user selection
        self.user_dict = system.get_user_dict()
        self.user_dict = {k: v for k, v in sorted(self.user_dict.items(), key=lambda item: item[1].lower())}
        self.user_id_list = list(self.user_dict.keys())
        self.user_id_list_curr_pos = None
        self.gui.main_user_pushButton.setText('---')
        
        # Autoconso state
        self.set_autoconso_state(True)
            
        # Warnings
        self.gui.update_system_infos_signal.emit()
        
        
        
    def stop(self):
        
        ''' Uninitialize panel '''
        
        # Disconnect rfid signal
        self.gui.rfid_tag_detected_signal.disconnect(self.tag_detected_callback)
        
        
        
    # TAG
    # =========================================================================
    
    def tag_detected_callback(self,tag):
        
        if tag == config['ADMIN']['tag'] :
            self.gui.switch_panel_signal.emit('admin')
            
        elif tag in system.list_tags() :
            ID = system.get_user_id_by_tag(tag)
            self.enter_account(ID)
            
        else : 
            self.gui.widgets['new_user'].tag = tag
            self.gui.switch_panel_signal.emit('new_user')
        
    
    # Admin
    # =========================================================================
    
    def admin_button_pressed(self):
        
        ''' Ask admin password to enter admin panel '''
        
        keyboard = self.gui.widgets['keyboard']
        keyboard.return_panel = 'main'
        keyboard.callback_end = self.admin_password_return
        keyboard.text_function = lambda value : "Enter admin password:"
        keyboard.requested_type = str
        self.gui.switch_panel_signal.emit('keyboard') 
        
        
    def admin_password_return(self,password):

        ''' Check admin password and make opening admin panel '''
        
        if password == config['ADMIN']['password'] :
            self.gui.widgets['keyboard'].return_panel = 'admin' # will be switched just after by keyboard
        

    
    
    
    # Warnings
    # =========================================================================
    
    def update_system_infos(self):
        
        ''' Update system infos '''
        
        warnings = system.get_warnings()
        if len(warnings)>0 : 
            system_infos = '\n'.join(warnings)
            self.gui.main_warnings_textEdit.setStyleSheet('color: red')
        else : 
            system_infos = 'Everything is fine!'
            self.gui.main_warnings_textEdit.setStyleSheet('color: green')
        self.gui.main_warnings_textEdit.setText(system_infos)
            
    
    
    # Autoconso state
    # =========================================================================

    def set_autoconso_state(self,state):
        
        ''' Set autoconso state '''
        
        if state is False :
            self.gui.main_autoconso_label.setStyleSheet('color: red')
            self.gui.main_autoconso_label.setText('DISABLED')
            self.gui.countdown.start()
        else : 
            self.gui.countdown.stop()
            self.gui.main_autoconso_label.setStyleSheet('color: green')
            self.gui.main_autoconso_label.setText('ENABLED')
            self.gui.main_disable_pushButton.setText('Disable')
            
        self.autoconso_state = state
        
        
    def switch_autoconso_state(self):
        
        ''' Switch autoconso state '''
        
        self.set_autoconso_state(not self.autoconso_state)


    # User manual selection
    # -------------------------------------------------------------------------
    
    def next_user(self):
        
        ''' Set next user in manual selection box '''
        
        if len(self.user_id_list)>0 :
            if self.user_id_list_curr_pos is None : 
                self.user_id_list_curr_pos = 0
            else : 
                self.user_id_list_curr_pos = (self.user_id_list_curr_pos + 1) % len(self.user_id_list)
            self.update_user_button_label()
        
        
    def previous_user(self):
        
        ''' Set previous user in manual selection box '''
        
        if len(self.user_id_list)>0 :
            if self.user_id_list_curr_pos is None : 
                self.user_id_list_curr_pos = len(self.user_id_list)-1
            else : 
                self.user_id_list_curr_pos = (self.user_id_list_curr_pos - 1) % len(self.user_id_list)
            self.update_user_button_label()
        
        
    def update_user_button_label(self):
        
        ''' Update user button label '''
        
        if len(self.user_id_list)>0 :
            ID = self.user_id_list[self.user_id_list_curr_pos]
            if User(ID).is_active() :
                self.gui.main_user_pushButton.setStyleSheet('color: black')
            else :
                self.gui.main_user_pushButton.setStyleSheet('color: gray')
            name = self.user_dict[ID]
            self.gui.main_user_pushButton.setText(f'{name} ({ID})')       
        
        
    def user_button_clicked(self):
        
        ''' Load user and open account panel '''
        
        if self.user_id_list_curr_pos is not None : 
            ID = self.user_id_list[self.user_id_list_curr_pos]
            self.enter_account(ID)
    
    
    
    # Enter account
    # -------------------------------------------------------------------------
    
    def enter_account(self,ID):
        
        ''' Open account panel and make a conso if autoconso enabled '''
    
        self.gui.current_user = User(ID)
        self.gui.switch_panel_signal.emit('account')
        if self.autoconso_state is True :
            self.gui.widgets['account'].add_conso()
    
    
    
    
