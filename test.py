# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 16:03:31 2020

@author: qchat
"""

from api.database import System,User
system = System()
#user = User(12)
#system.add_user('dummy')

#user2 = User(max(system.get_user_dict().keys()))

#system.add_user('hh')
print('user dict: ',system.get_user_dict())




#
##user.set_name('Francesco')
#print('name: ',user.get_name())
#
##user.set_email('thjs@sls.fr')
#print('email: ',user.get_email())
#
#print('tag: ',user.get_tag())
##user.set_tag(user.get_tag())
#user.set_tag(user.get_tag()+1)
#
##user.set_auto_donation(0.04)
#print('autodonation: ',user.get_auto_donation())
#print('total donation: ',user.get_donations())
#print('curr year donation: ',user.get_donations(year=2020))
#
##user.add_conso()
#print('nb consos: ',user.get_consos_by_date(2020,3,22))
##user.recharge(4)
##user.recharge(-4)
#
##system.list_operations_id()
##system.is_operation_checked(375)
##system.set_operation_checked(375)
##system.set_operation_checked(375,state=False)
#
#print('consos value: ' ,user.get_consos_value())
#print('recharges value: ' ,user.get_recharges_value())
#print('balance: ' ,user.get_balance())
#
#print('global shares value:' , system.get_shares_value())
#print('global recharges value:' ,system.get_recharges_value())
#
##system.add_caps(30,10)
#system.add_caps(0,10)
#
#system.add_supplies(10)
#
#system.add_donation(2)
#print('global donations value:' , system.get_donations_value()) 
#print('users donations value:' , system.get_users_donations_value()) 
#print('donations to do:' , system.get_donation_todo())

