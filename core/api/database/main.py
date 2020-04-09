# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 08:21:39 2019

@author: qchat
"""

import os
from .interface import Database

database_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(os.path.dirname(__file__))))),'data','database.db')
database = Database(database_path)

    



        
