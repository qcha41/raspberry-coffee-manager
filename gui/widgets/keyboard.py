# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 20:36:13 2018

@author: qchat
"""

import string

class Keyboard :

    def __init__(self,gui):
        self.gui=gui
        self.callback = None
        self.value = None
        self.rawValue = ''
        self.lowerCase = False
        self.letters = [a for a in string.ascii_uppercase]
        self.mode = int
        
        self.autoLetterCase = True
        self.testFunction = None
        
        self.previousWidget = None

        
        for key in [str(i) for i in range(10)] + self.letters :
            getattr(self.gui,'keyboard_'+key+'_pushButton').clicked.connect(lambda checked, a=key: self.keyPressed(a))
        self.gui.keyboard_point_pushButton.clicked.connect(lambda checked, a='.': self.keyPressed(a))
        self.gui.keyboard_minus_pushButton.clicked.connect(lambda checked, a='-': self.keyPressed(a))
        self.gui.keyboard_arobase_pushButton.clicked.connect(lambda checked, a='@': self.keyPressed(a))
        self.gui.keyboard_erase_pushButton.clicked.connect(self.eraseButtonPressed)
        self.gui.keyboard_return_pushButton.clicked.connect(self.returnButtonPressed)
        self.gui.keyboard_validate_pushButton.clicked.connect(self.validateButtonPressed)
        self.gui.keyboard_maj_pushButton.clicked.connect(self.majButtonPressed)
        
        
    def setPreviousWidget(self, value):
        self.previousWidget = value
    
    def setQuery(self,text):
        self.gui.keyboard_text_label.setText(text)
        
    def setCallback(self,func):
        self.callback = func
        
    def setAutoLowerCase(self,value):
        self.autoLetterCase = value
        
    def setTestFunction(self,func):
        self.testFunction = func
        
    def reset(self):
        self.setPreviousWidget(None)
        self.setLowerCase(False)
        self.setAutoLowerCase(True)
        self.setCallback(None)
        self.setTestFunction(None)
        self.updateValue('',0)
        self.setQuery('')

    
    def start(self):
        self.updateValue(self.rawValue,len(self.rawValue))
        
        
    def returnButtonPressed(self):
        self.callback(None)
        self.gui.setPanel(self.previousWidget.panel)
        
    def validateButtonPressed(self):
        self.callback(self.value)
        self.gui.setPanel(self.previousWidget.panel)
        
        
        

        
    # MODE SELECTION
        
    def setMode(self,mode):
    
        self.mode = mode
    
        if mode == float :
            for key in [str(i) for i in range(10)]+['point','minus'] :
                getattr(self.gui,'keyboard_'+key+'_pushButton').setEnabled(True)
            for key in self.letters+['maj','arobase'] :
                getattr(self.gui,'keyboard_'+key+'_pushButton').setEnabled(False)
        elif mode == int :
            for key in [str(i) for i in range(10)]+['minus'] :
                getattr(self.gui,'keyboard_'+key+'_pushButton').setEnabled(True)
            for key in self.letters+['maj','point','arobase'] :
                getattr(self.gui,'keyboard_'+key+'_pushButton').setEnabled(False)
        elif mode == str :
            for key in self.letters+[str(i) for i in range(10)]+['maj','point','minus','arobase'] :
                getattr(self.gui,'keyboard_'+key+'_pushButton').setEnabled(True)
                

        
        
        
    # VALUE
    
    def updateValue(self,value,cursor) :
        
        # Prise en compte nouvelle value
        self.rawValue = value
        try : 
            self.value = self.mode(value)
        except : 
            self.value = None
        
        # Mise à jour retour
        self.updateGui()
        self.gui.keyboard_value_lineEdit.setCursorPosition(cursor)
        
        # Activation bouton Validate
        result = True
        if self.testFunction is not None : 
            result = self.testFunction(self.value)
        self.gui.keyboard_validate_pushButton.setEnabled(result)
               
    def updateGui(self):
        self.gui.keyboard_value_lineEdit.setText(self.rawValue)
        self.gui.keyboard_retourValue_label.setText('--> '+str(self.value))
        
    def getCursorPosition(self):
        return self.gui.keyboard_value_lineEdit.cursorPosition()
      
    def eraseButtonPressed(self):
        if self.rawValue != '' :
            pos = self.getCursorPosition()
            if pos != 0 :
                rawValue = self.rawValue[:pos-1]+self.rawValue[pos:]
                cursor = pos-1
                self.updateValue(rawValue,cursor)
        
    def keyPressed(self,key):
        if self.lowerCase is True :
            try : 
                key = key.lower()
            except :
                pass
        pos = self.getCursorPosition()
        rawValue = self.rawValue[:pos]+key+self.rawValue[pos:]
        cursor = pos+1
        self.updateValue(rawValue,cursor)
        
        if key in self.letters and self.autoLetterCase is True :
            self.autoLetterCase = False
            self.majButtonPressed()
        
        
        
        
    # MAJ
        
    def majButtonPressed(self):
        self.setLowerCase(not self.lowerCase)
    
    def setLowerCase(self,value):
        if value is True :
            for key in self.letters :
                getattr(self.gui,'keyboard_'+key+'_pushButton').setText(key.lower())
        else :
            for key in self.letters :
                getattr(self.gui,'keyboard_'+key+'_pushButton').setText(key.upper())
        self.lowerCase = value
        
        
        