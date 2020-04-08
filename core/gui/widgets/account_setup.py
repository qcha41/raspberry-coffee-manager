# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 08:58:14 2020

@author: qchat
"""



class AccountSetupPanel():
    
    def __init__(self,gui):
        
        self.gui = gui
        self.user = None
        
        # Connect signals
        self.gui.account_setup_return_pushButton.clicked.connect(self.return_pressed)
        self.gui.account_setup_active_checkBox.stateChanged.connect(self.active_state_changed)
        self.gui.account_setup_active_checkBox.clicked.connect(self.gui.countdown.start)
        self.gui.account_setup_name_pushButton.clicked.connect(self.name_button_pressed)
        self.gui.account_setup_email_pushButton.clicked.connect(self.email_button_pressed)
        self.gui.account_setup_shares_pushButton.clicked.connect(self.shares_button_pressed)
        self.gui.account_setup_increaseDonation_pushButton.clicked.connect(self.increase_donation)
        self.gui.account_setup_increaseDonation_pushButton.clicked.connect(self.gui.countdown.start)
        self.gui.account_setup_decreaseDonation_pushButton.clicked.connect(self.decrease_donation)
        self.gui.account_setup_decreaseDonation_pushButton.clicked.connect(self.gui.countdown.start)
        self.gui.account_setup_readtag_pushButton.clicked.connect(self.update_tag)
        self.gui.account_setup_readtag_pushButton.clicked.connect(self.gui.countdown.start)

        # Return countdown
        self.callback_countdown_update = lambda x : self.gui.account_setup_return_pushButton.setText(f'Return\n({x})')
        self.callback_countdown_end = self.return_pressed
        
        
        
    def start(self):
        
        ''' Initialize panel '''
        
        # Load current user
        self.user = self.gui.current_user
        
        # Display user infos
        self.gui.account_setup_ID_label.setText(str(self.user.ID))
        self.gui.account_setup_active_checkBox.setChecked(self.user.is_active())
        self.gui.account_setup_name_pushButton.setText(self.user.get_name())
        self.gui.account_setup_tag_label.setText(str(self.user.get_tag()))
        self.gui.account_setup_email_pushButton.setText(self.user.get_email())
        self.gui.account_setup_shares_label.setText(str(self.user.get_total_shares())+' \u20ac')
        self.update_donation_gui()
       
        
        # Active state for buttons
        self.active_state_changed()

        # Return button
        self.gui.countdown.start()
        

    
    def stop(self) :
        
        ''' Uninitialize panel '''
        
        pass
    
    
    
    
    # Buttons
    # =========================================================================   

    def update_tag(self):
        
        ''' Wait for tag and update it '''
        
        import numpy 
        new_tag = abs(int(numpy.random.randn()*1e7))
        self.user.set_tag(new_tag)
        self.gui.account_setup_tag_label.setText(str(self.user.get_tag()))
        
    
    def name_button_pressed(self):    
        
        ''' Start a keyboard request for user's name '''
        
        keyboard = self.gui.widgets['keyboard']
        keyboard.return_panel = 'account_setup'
        keyboard.callback_end = self.user.set_name
        keyboard.text_function = lambda value : f"Set name as {value}"
        keyboard.requested_type = str
        keyboard.test_function = lambda x : x != ''
        keyboard.value = self.user.get_name()
        self.gui.switch_panel_signal.emit('keyboard') 
        
        
    def email_button_pressed(self):   
        
        ''' Start a keyboard request for user's email '''
        
        keyboard = self.gui.widgets['keyboard']
        keyboard.return_panel = 'account_setup'
        keyboard.callback_end = self.user.set_email
        keyboard.text_function = lambda value : f"Set email as\n{value}"
        keyboard.requested_type = str
        keyboard.test_function = lambda x : '@' in x
        keyboard.value = self.user.get_email()
        self.gui.switch_panel_signal.emit('keyboard') 
        
        
    def shares_button_pressed(self):    
        
        ''' Start a keyboard request to add shares '''
        
        keyboard = self.gui.widgets['keyboard']
        keyboard.return_panel = 'account_setup'
        keyboard.callback_end = self.user.add_shares
        keyboard.text_function = lambda value : f"Add {value} \u20ac shares"
        keyboard.requested_type = float
        total_shares = self.user.get_total_shares()
        keyboard.test_function = lambda x : (x != 0) and ((total_shares+x)>=0)
        self.gui.switch_panel_signal.emit('keyboard') 
        
        
    def increase_donation(self):
        
        ''' Increase current auto donation by 0.01E '''
        
        curr_donation = self.user.get_auto_donation()
        self.user.set_auto_donation(curr_donation + 0.01)
        self.update_donation_gui()
        
        
    def decrease_donation(self):
        
        ''' Decrease current auto donation by 0.01E if the result is positive or 0 '''
        
        curr_donation = self.user.get_auto_donation()
        if curr_donation - 0.01 >= 0 :
            self.user.set_auto_donation(curr_donation - 0.01)
            self.update_donation_gui()

            
    def update_donation_gui(self):
        
        ''' Update donation value on the GUI '''
        
        self.gui.account_setup_donation_label.setText(str(self.user.get_auto_donation())+' \u20ac')
        
        
    
    # Active state
    # =========================================================================
    
    def set_active_state(self,state):
        
        ''' Enable or disable the buttons '''
    
        self.gui.account_setup_name_pushButton.setEnabled(state)
        self.gui.account_setup_readtag_pushButton.setEnabled(state)
        self.gui.account_setup_email_pushButton.setEnabled(state)
        self.gui.account_setup_shares_pushButton.setEnabled(state)
        self.gui.account_setup_decreaseDonation_pushButton.setEnabled(state)
        self.gui.account_setup_increaseDonation_pushButton.setEnabled(state)
            
            
    def active_state_changed(self):
        
        ''' Read active state and propagate it to the database + GUI '''
        
        state = self.gui.account_setup_active_checkBox.isChecked()
        self.set_active_state(state)
        self.user.set_active(state)
        
        
    # Return
    # =========================================================================
    
    def return_pressed(self):
        
        ''' Open account panel '''
        
        self.gui.switch_panel_signal.emit('account') 
        