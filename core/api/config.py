# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 17:46:05 2019

@author: qchat
"""

import configparser
import os

def load_config():
    
    ''' Loads and returns the content of the configuration file '''
    
    current_script_path = os.path.realpath(os.path.dirname(__file__))
    config_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(current_script_path))),'data','config.ini')
    
    print(os.get_cwd())
    
    if os.path.exists(config_file_path) is True : 
        config = configparser.ConfigParser()
        config.read(config_file_path)
    else :
        raise ValueError("Configuration file missing in data folder")
    
    return config
        