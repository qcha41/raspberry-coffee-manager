# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 20:29:10 2018

@author: qchat
"""
import os 
import random 
import time

class Images :

    def __init__(self,sdk) :
    
        self.folderPath = os.path.join(sdk.dataFolderPath,'images')
        self.pathList = None
        self.loadPaths()
        
    def getRandomImagePath(self,folder):
        while True :
            try :
                self.loadPaths(folder=folder)
                result = random.choice(self.pathList)
                break
            except :
                time.sleep(0.2)
        return result
            
    
    def loadPaths(self,folder=None):
        
        if folder is None :
            self.pathList = []
            for subfolder in os.listdir(self.folderPath) :
                self.pathList += [os.path.join(self.folderPath,subfolder,e) for e in os.listdir(os.path.join(self.folderPath,subfolder))]
        else :
            self.pathList = [os.path.join(self.folderPath,folder,e) for e in os.listdir(os.path.join(self.folderPath,folder))]