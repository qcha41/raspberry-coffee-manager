#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 11:13:09 2018

@author: pi
"""

import smtplib
from email.message import EmailMessage

from threading import Thread


class Email():
    
    def __init__(self,sdk):
        self.sdk = sdk
    
    def send(self,address,subject,message):
        sender = Sender(address,subject,message)
        sender.start()
        
    def negativeBalance(self,address,username,balance) :
        if self.sdk.var.getValue('email') is True :
            subject = 'Negative balance (%g \u20ac), please charge your account'%balance
            message = '''Hi %s,\n
Your coffee account has a negative balance (%g \u20ac), please charge it. You can use these ways:
- SEPA Bank transfer:   IBAN: GB95 REVO 0099 7007 2546 45    BIC: REVOGB21
- Revolut: 06.01.87.97.61
- Paypal: https://www.paypal.me/quentinchateiller (specify 'personal' to avoid fees)
- Cash: In the box near the manager
Then, do not forget to notify it in your user account.\n
PS : If you are a daily user, please always keep your balance >10 \u20ac to maintain a sufficient working capital (to buy caps in advance, in large quantity at low price).''' %(username,balance+0)
            self.send(address,subject,message)   
            
    def lowBalance(self,address,username) :
        if self.sdk.var.getValue('email') is True :
            subject = "Balance <10\u20ac, it's ok, but consider charging your account"
            message = '''Hi %s,\n
Your coffee account just went below 10\u20ac, which is still ok, but consider charging it to maintain a sufficient working capital (to buy caps in advance, in large quantity at low price). You can use these ways:
- SEPA Bank transfer:   IBAN: GB95 REVO 0099 7007 2546 45    BIC: REVOGB21
- Revolut: 06.01.87.97.61
- Paypal: https://www.paypal.me/quentinchateiller (specify 'personal' to avoid fees)
- Cash: In the box near the manager
Then, do not forget to notify it in your user account.''' %(username)
            self.send(address,subject,message)           
        
    def notifyRecharge(self,username,value,prevBalance,newBalance):
        subject = "%s's account recharged (%g \u20ac)"%(username,value)
        message = 'Previous balance : %g \u20ac\n'%prevBalance
        message += 'New balance : %g \u20ac\n\n'%newBalance
        self.send('q.chateiller@gmail.com',subject,message)   
        
        
      
        
    def sendError(self,message):
        subject = 'Coffee manager just crashed'
        self.send('q.chateiller@gmail.com',subject,message)
        
    def newUser(self,username):    
        subject = 'New username %s'%username
        self.send('q.chateiller@gmail.com',subject,'Update the email!')
    
    
         
            
            
class Sender(Thread):
        
    def __init__(self,address,subject,message):
        Thread.__init__(self)
        self.address = address
        self.subject = subject
        self.message = message+'\n\nSee you! ;)\n\n\n\n\n[This message has been sent automatically, please do not reply]'
        
    def run(self):
        try :
            msg = EmailMessage() 
            msg.set_content(self.message)
            msg['Subject'] = self.subject
            msg['From'] = 'ToniQ Coffee Manager'
            msg['To'] = self.address
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("coffeemanagerC2N@gmail.com", "sandwich91")
            server.sendmail("coffeemanagerC2N@gmail.com",self.address,msg.as_string())
            server.quit()
        except :
            pass
        