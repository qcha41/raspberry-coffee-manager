# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 20:36:13 2018

@author: qchat
"""

# Setting current directory
import os
currDir = os.path.realpath(os.path.dirname(__file__))
os.chdir(currDir)

debugMode = False 

import traceback, time, sys
from PyQt5.QtWidgets import QApplication

def errorDetected(exctype, value, tb):
    errorStr = str(exctype)+' '+str(value)+'\n'+''.join(traceback.format_tb(tb))
    print(errorStr)
    sdk.email.sendError(errorStr)
    time.sleep(2)
    if debugMode is False :
        sdk.system.restart() 

sys.excepthook = errorDetected

from sdk.main import SDK
sdk = SDK()

from gui.main import GUI
app = QApplication(sys.argv)
gui = GUI(sdk)
gui.show()
app.exec_()
    