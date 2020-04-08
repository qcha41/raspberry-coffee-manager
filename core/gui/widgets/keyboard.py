# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 14:47:49 2020

@author: qchat
"""

import string

class KeyboardPanel():
    
    def __init__(self,gui):
        
        self.gui = gui
        self.letters = [a for a in string.ascii_uppercase]
        
        # Connect signals
        for key in [str(i) for i in range(10)] + self.letters :
            getattr(self.gui,'keyboard_'+key+'_pushButton').clicked.connect(lambda checked, a=key: self.key_pressed(a))
            getattr(self.gui,'keyboard_'+key+'_pushButton').clicked.connect(self.gui.countdown.start)
        self.gui.keyboard_point_pushButton.clicked.connect(lambda checked : self.key_pressed('.'))
        self.gui.keyboard_point_pushButton.clicked.connect(self.gui.countdown.start)
        self.gui.keyboard_minus_pushButton.clicked.connect(lambda checked : self.key_pressed('-'))
        self.gui.keyboard_minus_pushButton.clicked.connect(self.gui.countdown.start)
        self.gui.keyboard_arobase_pushButton.clicked.connect(lambda checked : self.key_pressed('@'))
        self.gui.keyboard_arobase_pushButton.clicked.connect(self.gui.countdown.start)
        self.gui.keyboard_space_pushButton.clicked.connect(lambda : self.key_pressed(' '))
        self.gui.keyboard_space_pushButton.clicked.connect(self.gui.countdown.start)
        self.gui.keyboard_erase_pushButton.clicked.connect(self.erase_button_pressed)
        self.gui.keyboard_erase_pushButton.clicked.connect(self.gui.countdown.start)
        self.gui.keyboard_return_pushButton.clicked.connect(self.return_button_pressed)
        self.gui.keyboard_validate_pushButton.clicked.connect(self.validate_button_pressed)
        self.gui.keyboard_maj_pushButton.clicked.connect(self.maj_button_pressed)
        self.gui.keyboard_maj_pushButton.clicked.connect(self.gui.countdown.start)
        
        # Initialise variables
        self.reset()
        
        # Return countdown
        self.callback_countdown_update = lambda x : self.gui.keyboard_return_pushButton.setText(f'Return\n({x})')
        self.callback_countdown_end = self.return_button_pressed
        
        
    def reset(self):
        
        ''' Reset keyboard variables '''
        
        self.return_panel = None
        self.callback_end = None
        self.text_function = None
        self.requested_type = None
        self.test_function = None
        self.auto_letter_case = True
        self.lower_case = False
        self.raw_input = ''
        self.value = None
        self.auto_return = True
        

    def start(self):   
        
        ''' Initialize panel '''
         
        if self.value is not None: 
            self.update_value(str(self.value),len(str(self.value)))
        else :
            self.update_value('',0)
            
        self.update_buttons_states()
        
        # Return button
        self.gui.countdown.start()
        
        
    def stop(self):
        
        ''' Uninitialize panel '''
        
        self.reset()    
        
    
    def update_buttons_states(self):
        
        ''' Enable / Disable key buttons regarding the requested type '''
        
        if self.requested_type == float :
            for key in [str(i) for i in range(10)]+['point','minus'] :
                getattr(self.gui,'keyboard_'+key+'_pushButton').setEnabled(True)
            for key in self.letters+['maj','arobase','space'] :
                getattr(self.gui,'keyboard_'+key+'_pushButton').setEnabled(False)
        elif self.requested_type == int :
            for key in [str(i) for i in range(10)]+['minus'] :
                getattr(self.gui,'keyboard_'+key+'_pushButton').setEnabled(True)
            for key in self.letters+['maj','point','arobase','space'] :
                getattr(self.gui,'keyboard_'+key+'_pushButton').setEnabled(False)
        elif self.requested_type == str :
            for key in self.letters+[str(i) for i in range(10)]+['maj','point','minus','arobase'] :
                getattr(self.gui,'keyboard_'+key+'_pushButton').setEnabled(True)
                

    def key_pressed(self,key):
        
        ''' Add the given key in the raw_input variable at the right place '''
        
        # Process raw entry
        if self.lower_case is True :
            try : key = key.lower()
            except : pass
        pos = self.get_cursor_position()
        self.update_value(self.raw_input[:pos]+key+self.raw_input[pos:],pos+1)
        
        # Auto letter case for two first characters
        if key in self.letters and self.auto_letter_case is True :
            self.maj_button_pressed()
            
            
    def get_cursor_position(self):
        
        ''' Returns current cursor position in the raw input '''
        
        return self.gui.keyboard_value_lineEdit.cursorPosition()
      
        
    def erase_button_pressed(self):
        
        ''' Remove the character located at the left of the cursor in the raw input '''
        
        # Erase
        if self.raw_input != '' :
            pos = self.get_cursor_position()
            if pos != 0 :
                self.update_value(self.raw_input[:pos-1]+self.raw_input[pos:],pos-1)
        
        
    def update_gui_values(self):
        
        ''' Update raw input and value in the GUI '''
        
        self.gui.keyboard_value_lineEdit.setText(self.raw_input)
        self.gui.keyboard_text_label.setText(self.text_function(self.value))
        
        
    def update_value(self,raw_input,cursor_position) :
        
        ''' Update raw input and cursor position '''
        
        # Prise en compte nouvelle value
        self.raw_input = raw_input
        try : 
            self.value = self.requested_type(self.raw_input)
            if self.requested_type == float : self.value = round(self.value,2)
        except : self.value = None
        
        # Mise à jour GUI
        self.update_gui_values()
        self.gui.keyboard_value_lineEdit.setCursorPosition(cursor_position)
        
        # Activation bouton Validate
        if self.value is None :
            result = False
        else :
            if self.test_function is not None : 
                result = self.test_function(self.value)
            else :
                result = True
        self.gui.keyboard_validate_pushButton.setEnabled(result)
        
        
    # Return and validate buttons
    # =========================================================================
    
    def return_button_pressed(self):
        
        ''' Return to selected panel '''

        self.gui.switch_panel_signal.emit(self.return_panel)
        
        
    def validate_button_pressed(self):
        
        ''' Execute callback_end function and return to selected panel '''
        
        auto_return = self.auto_return # important, because callback_end can change it
        self.callback_end(self.value)
        if auto_return is True :
            self.return_button_pressed()
        
    # MAJ
    # =========================================================================
        
    def maj_button_pressed(self):
        
        ''' Swith MAJ state '''
        
        self.set_lower_case(not self.lower_case)
        self.auto_letter_case = False
    
    
    def set_lower_case(self,state):
        
        ''' Enable / Disable lower case state '''
        
        if state is True :
            for key in self.letters :
                getattr(self.gui,'keyboard_'+key+'_pushButton').setText(key.lower())
        else :
            for key in self.letters :
                getattr(self.gui,'keyboard_'+key+'_pushButton').setText(key.upper())
        self.lower_case = state
        