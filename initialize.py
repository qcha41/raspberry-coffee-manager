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
maxDelay = 40 #s
result = False
i = 0
while time.time()-tini < maxDelay :
    if os.system('ping -c1 google.com') == 0 :
        result = True
        break
    else :
        i+=1
        time.sleep(0.1)
        print('Waiting for an internet connection, please wait... (%i)'%round(maxDelay-(time.time()-tini)),end="\r")
print()
print('Connected to internet!')
print()


# Update git directory
print('Updating git repository...')
ans = git.Repo().git.pull()
print(ans)
print('Update finished!')
print()


time.sleep(50)