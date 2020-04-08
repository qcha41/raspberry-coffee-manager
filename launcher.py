# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 20:36:13 2018

@author: qchat
"""

auto_reboot = False 

import traceback, time, sys
from core.api import email,system

def errorDetected(exctype, value, tb):
    errorStr = str(exctype)+' '+str(value)+'\n'+''.join(traceback.format_tb(tb))
    print(errorStr)
    email.notify_error(errorStr)
    time.sleep(2)
    if auto_reboot is True :
        system.reboot() 

sys.excepthook = errorDetected

from PyQt5.QtWidgets import QApplication
from core.gui.main import GUI
app = QApplication(sys.argv)
gui = GUI()
gui.show()
app.exec_()
    