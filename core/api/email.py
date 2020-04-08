#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 11:13:09 2018

@author: pi
"""

import smtplib
from email.message import EmailMessage

from threading import Thread

from . import config


    
def notify_negative_balance(email,username,balance) :
    subject = f'Negative balance on your coffee account ({balance}\u20ac), please recharge it ASAP !'
    message = f'Hi {username},\n\n'
    message += f'Your coffee account has a negative balance ({balance} \u20ac), please recharge it ASAP ! Then, do not forget to notify it in your user account.\n'
    message += 'In the future, please always keep your balance positive, to avoid reducing the ability of the admin to buy new caps at a good price.\n\n'
    message += 'See you!'
    Thread( target = send, args = (email,subject,message) ).start()
        
 
    
def notify_error(error_message):
    email = config['ADMIN']['email']
    subject = 'Coffee manager just crashed'
    Thread( target = send, args = (email,subject,error_message) ).start()


def test():
    email = config['ADMIN']['email']
    subject = 'Test'
    message = 'Test'
    Thread( target = send, args = (email,subject,message) ).start()

     
def send(email,subject,message):
    message = message+'\n\n\n\n\n[This message has been sent automatically, please do not reply]'
    try :
        msg = EmailMessage() 
        msg.set_content(message)
        msg['Subject'] = subject
        msg['From'] = config['GENERAL']['system_name']
        msg['To'] = email
        server = smtplib.SMTP(config['EMAIL']['smtp_server'], int(config['EMAIL']['smtp_port']))
        server.starttls()
        server.login(config['EMAIL']['smtp_username'], config['EMAIL']['smtp_password'])
        server.sendmail(config['EMAIL']['smtp_username'],email,msg.as_string())
        server.quit()
    except :
        pass
        