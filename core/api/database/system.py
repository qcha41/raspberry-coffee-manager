# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 20:35:55 2020

@author: qchat
"""

from .. import config
from .main import database
from .users import User
from . import utilities



# Users
# =========================================================================

def add_user(name):
    
    ''' Add a new user to the database with the provided name '''
    
    assert isinstance(name,str), "The user name as to be a string"
    default_donation = float(config['DONATION']['user_auto_default'])
    database.write("INSERT INTO users (name,auto_donation) VALUES ('%s',%g)"%(name,default_donation)) 
        
    
def get_user_dict(only_active=False):
    
    ''' Returns a dictionnary containing the user IDs (key) and their name (value) '''
    
    constraint = ''
    if only_active is True : constraint = 'WHERE active=1'
    
    ans = database.read("SELECT id,name FROM users "+constraint)
    return ans.set_index('id')['name'].to_dict()


def list_users_balance():
    
    ''' Returns tha balance of all users in a dictionnary '''
    
    user_dict = get_user_dict()    
    for key in user_dict : 
        user_dict[key] = User(key).get_balance()
    return user_dict


def list_tags():
    
    ''' Returns a tuple with all active RFID tags '''
    
    return tuple(database.read("""SELECT tag FROM users
                                   WHERE tag IS NOT NULL""").tag)
    

def get_nb_users(only_active=False):
    
    ''' Returns number of active users '''
    
    constraint = ''
    if only_active is True : constraint = 'WHERE active=1'
    
    return int(database.read("""SELECT count(id) FROM users """+constraint).iloc[0]['count(id)'])
    
    
# Accounts operations
# =========================================================================

def get_accounts_balance():
    
    ''' Returns the global balance of the account_operations table '''
    
    result = database.read("""SELECT sum(value) FROM account_operations""").iloc[0]['sum(value)']
    if result is not None : return round(result,2)
    else : return 0 

    
    
def get_total_shares():
    
    ''' Returns the total value of the shares '''
    
    result = database.read("""SELECT sum(value) FROM account_operations
                              WHERE label ='Shares'""").iloc[0]['sum(value)']
    if result is not None : return round(result,2)
    else : return 0 

    
def get_total_recharges():
    
    ''' Returns the total value of the recharges '''
    
    result = database.read("""SELECT sum(value) FROM account_operations
                              WHERE label ='Recharge'""").iloc[0]['sum(value)']
    if result is not None : return round(result,2)
    else : return 0 
    
    
    
    
def list_account_operations_id():
    
    ''' Returns a tuple with all account operations IDs '''
    
    return tuple(database.read("""SELECT id FROM account_operations""")['id'])

#    

def is_account_operation_checked(ID):
    
    ''' Returns True/False whether the account operation with this ID is checked or not '''
    
    assert isinstance(ID,int), "The account operation ID has to be an integer"
    assert ID in list_account_operations_id(), "This account operation ID does not exist"
    result = bool(database.read(f"""SELECT checked FROM account_operations
                                    WHERE id={ID}""").iloc[0]['checked'])
    return result



def set_account_operation_checked( ID, state=True):
    
    ''' Set the checked state of the account operation with this ID, default is True '''
    
    assert isinstance(ID,int), "The account operation ID has to be an integer"
    assert ID in list_account_operations_id(), "This account operation ID does not exist"
    assert isinstance(state,bool), "The checked state has to be a boolean"
    
    database.write(f"""UPDATE account_operations
                       SET checked = {int(state)}
                       WHERE id={ID}""")
    

def get_account_operations():
    result = database.read("""SELECT account_operations.id,timestamp,label,users.name,value,checked FROM account_operations
                            INNER JOIN users       
                            ON account_operations.user=users.id""")
    result.rename(columns={"name": "user"},inplace=True)
    return result

    
# Caps operations
# ==========================================================================

def get_caps_balance():
    
    ''' Returns the global balance of the caps_operations table '''
    
    result = database.read("""SELECT sum(value) FROM caps_operations""").iloc[0]['sum(value)']
    if result is not None : return round(result,2)
    else : return 0 
    
    
def get_caps_balance_users():
    
    ''' Returns the sum of caps operations that is associated to users'''

    result = database.read("""SELECT sum(value) FROM caps_operations
                              WHERE user IS NOT NULL """).iloc[0]['sum(value)']
    if result is not None : return round(result,2)
    else : return 0 
    
    
def get_caps_balance_system():
    
    ''' Returns the sum of caps operations that is not associated to users'''
    
    result = database.read("""SELECT sum(value) FROM caps_operations
                              WHERE user IS NULL """).iloc[0]['sum(value)']
    if result is not None : return round(result,2)
    else : return 0


def get_caps_remaining():
    
    ''' Returns the number of remaining caps in the stock '''
   
    result = database.read("""SELECT sum(qty) FROM caps_operations""").iloc[0]['sum(qty)']
    if result is not None : return int(result)
    else : return 0 
    
def get_caps_remaining_system():
    
    ''' Returns the number of remaining caps in the stock '''
   
    result = database.read("""SELECT sum(qty) FROM caps_operations
                              WHERE user IS NULL""").iloc[0]['sum(qty)']
    if result is not None : return int(result)
    else : return 0 
    
def get_caps_remaining_users():
    
    ''' Returns the number of remaining caps in the stock '''
   
    result = database.read("""SELECT sum(qty) FROM caps_operations
                              WHERE user IS NOT NULL""").iloc[0]['sum(qty)']
    if result is not None : return int(result)
    else : return 0 
    
def get_caps_price() :
    
    ''' Returns the current caps price for users '''
    
    caps_remaining = get_caps_remaining()
    if caps_remaining > 0 :    
        return round(-get_caps_balance()/caps_remaining,2)
    else :
        return None
    

def add_caps_operation(label,qty,value):
    
    ''' Add a new general caps operation '''
    
    assert isinstance(label,str), "The label of this operation has to be a string"
    assert isinstance(qty,int), "The quantity of caps of this operation has to be an integer"
    assert isinstance(value,int) or isinstance(value,float), "The value of this operation has to be a number (int/float)"
    
    timestamp = utilities.get_timestamp()
    value = round(float(value),2)
    database.write(f'''INSERT INTO caps_operations (timestamp,label,qty,value)
                        VALUES ('{timestamp}','{label}',{qty},{value})''')

    
def add_caps_purchase(qty,price):
    
    ''' Add a new caps purchase '''
    
    assert isinstance(qty,int), "The quantity of caps of this caps purchase has to be an integer"
    assert qty != 0, "The quantity of caps of this caps purchase has to be different from zero"
    assert isinstance(price,int) or isinstance(price,float), "The price of this caps purchase has to be a number (int/float)"

    add_caps_operation('Caps purchase',qty,-price)



def add_supplies_purchase(price):
    
    ''' Records a supplies purchase '''
    
    assert isinstance(price,int) or isinstance(price,float), "The price of the supplies has to be a number (int/float)"
    assert price != 0, "The price of the supplies has to be different from zero"

    add_caps_operation('Supplies purchase',0,-price)
    
    
    
def remove_missing_caps(qty):
    
    ''' Records a missing caps qty '''
    
    assert isinstance(qty,int), "The quantity of missing caps has to be an integer"
    assert qty != 0, "The quantity of missing caps has to be different from zero"

    add_caps_operation('Missing caps',-qty,0)
    
    
 
    
    
def get_system_caps_operations():
    return database.read("""SELECT timestamp,label,qty,value FROM caps_operations
                              WHERE user IS NULL""")
    
        
# Donations operations
# ==========================================================================

def add_donation_operation(label,value):
    
    ''' Add a new donation operation '''
    
    assert isinstance(label,str), "The label of this donation operation has to be a string"
    assert isinstance(value,int) or isinstance(value,float), "The donation value has to be a number (int/float)"
    assert value != 0
    
    timestamp = utilities.get_timestamp()
    value = round(float(value),2)
    database.write(f'''INSERT INTO donation_operations (timestamp,label,value)
                        VALUES ('{timestamp}','{label}',{value})''')
        
    
def add_charity_donation(donation):
    
    ''' Records a charity donation '''
    
    assert isinstance(donation,int) or isinstance(donation,float), "The donation value has to be a number (int/float)"
    assert donation != 0, "The donation value has to be different from zero"
    add_donation_operation('To charity',-donation)



def get_donation_balance():
    
    ''' Returns the donation balance (ie what remains to be donated to a charity)'''
    
    result = database.read("""SELECT sum(value) FROM donation_operations""").iloc[0]['sum(value)']
    if result is not None : return round(result,2)
    else : return 0 
    

def get_system_donation_balance():
    
    ''' Returns the sum of donation operations that is not associated to users'''
    
    result = database.read("""SELECT sum(value) FROM donation_operations
                              WHERE user IS NULL """).iloc[0]['sum(value)']
    if result is not None : return round(result,2)
    else : return 0 
    

def get_users_donation_balance():
    
    ''' Returns the sum of donation operations that is associated to users'''
    
    result = database.read("""SELECT sum(value) FROM donation_operations
                              WHERE user IS NOT NULL """).iloc[0]['sum(value)']
    if result is not None : return round(result,2)
    else : return 0 
    

def get_system_donation_operations():
    return database.read("""SELECT timestamp,label,value FROM donation_operations
                              WHERE user IS NULL""")
    
# Balance
# ==========================================================================

def get_balance():
    
    ''' Returns the global balance of the system (ie what should appears in the bank account) '''
   
    # Gain : User payments in general
    user_payments = get_accounts_balance()
    
    # Losses : caps (+ supplies) + donation
    caps_supplies_system_balance = get_caps_balance_system()
    donations_system_balance = get_system_donation_balance()

    # Sumup
    result = user_payments + caps_supplies_system_balance + donations_system_balance
    if result is not None : return round(result,2)
    else : return 0 
    
        
    
def get_warnings() :
    
    balance_list = []
    shares_list = []
    
    user_dict = get_user_dict(only_active=True)
    for key in user_dict : 
        user = User(key)
        balance = user.get_balance()
        if balance < 0 : balance_list.append(f'{user_dict[key]}: {balance} \u20ac')
        shares = user.get_total_shares()
        if shares == 0 : shares_list.append(f'{user_dict[key]}: No shares')
        
    return balance_list + shares_list
    