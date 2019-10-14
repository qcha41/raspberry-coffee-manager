# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 19:59:58 2019

@author: qchat
"""

print()
print('   ================')
print('    COFFEE MANAGER ')
print('   ================')
print()
print('Application starting, please wait...')
print('')


import os
import time
import git

# Waiting for incoming connection
print('Waiting for an internet connection, please wait...',end="\r")
tini = time.time()
maxDelay = 30 #s
result = False
while time.time()-tini < maxDelay :
    if os.system('ping -c1 google.com') == 0 :
        result = True
        break
    else :
        print('Waiting for an internet connection, please wait... (%i)'%round(maxDelay-(time.time()-tini)),end="\r")
        time.sleep(1)
        
        
if result is True :
    print()
    print('Connected to internet!')
    print()
    
    # Update git directory
    print('Updating git repository...')
    time.sleep(3)
    ans = git.Repo().git.pull()
    print(ans)
    print('Update finished!')
    print()
    
    # Starting GUI
    print('Starting GUI...')
    exec(open("./interface.py").read())
    
else :
    # Restart pi
    print('Impossible to establish a connection. System restarting...')
    time.sleep(3)
    os.system('sudo shutdown -r now')
