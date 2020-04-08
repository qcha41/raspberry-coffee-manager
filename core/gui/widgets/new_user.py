# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 09:38:01 2020

@author: qchat
"""

from ...api.database import system
from ...api.database.users import User



class NewUserPanel:
    
    def __init__(self,gui):
        
        self.gui = gui
        
        # Connect signals
        self.gui.new_user_return_pushButton.clicked.connect(self.return_pressed)
        self.gui.new_user_confirm_pushButton.clicked.connect(self.confirm_pressed)
        
        # Return countdown
        self.callback_countdown_update = lambda x : self.gui.new_user_return_pushButton.setText(f'Return\n({x})')
        self.callback_countdown_end = self.return_pressed
        
        
    def start(self):
        
        ''' Initialize panel '''
        
        # Return button
        self.gui.countdown.start()
        
        
    def stop(self):
        
        ''' Uninitialize panel '''
        
        pass
    
    
    def confirm_pressed(self):
        
        ''' Create a new user '''
        
        # Create new user
        system.add_user('')
        ID = max(system.get_user_dict().keys())
        self.gui.current_user = User(ID)
        self.gui.switch_panel_signal.emit('account_setup')
        
        
    def return_pressed(self):
        
        ''' Return to main panel '''
        
        self.gui.switch_panel_signal.emit('main') 
        