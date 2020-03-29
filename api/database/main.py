# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 08:21:39 2019

@author: qchat
"""

import datetime as dt
import pandas as pd

from .. import config
from .interface import Database
database = Database(config['GENERAL']['database_path'])


class System :
    
    # Users
    # =========================================================================
    
    def add_user(self,name):
        
        ''' Add a new user to the database with the provided name '''
        
        assert isinstance(name,str), "The user name as to be a string"
        default_donation = float(config['DONATION']['user_auto_default'])
        database.write("INSERT INTO users (name,auto_donation) VALUES ('%s',%g)"%(name,default_donation)) 
            
        
    def get_user_dict(self):
        
        ''' Returns a dictionnary containing the user IDs (key) and their name (value) '''
        
        ans = database.read("SELECT id,name FROM users")
        return ans.set_index('id')['name'].to_dict()
    
    
    def list_users_balance(self):
        
        ''' Returns tha balance of all users in a dictionnary '''
        
        user_dict = self.get_user_dict()    
        for key in user_dict : 
            user_dict[key] = User(key).get_balance()
        return user_dict
    
    
    def list_tags(self):
        
        ''' Returns a tuple with all active RFID tags '''
        
        return tuple(database.read("""SELECT tag FROM users
                                       WHERE tag IS NOT NULL""").tag)
        
        
    # Accounts operations
    # =========================================================================
    
    def get_accounts_balance(self):
        
        ''' Returns the global balance of the account_operations table '''
        
        result = database.read("""SELECT sum(value) FROM account_operations""").iloc[0]['sum(value)']
        if result is not None : return round(result,2)
        else : return 0 

        
        
    def get_total_shares(self):
        
        ''' Returns the total value of the shares '''
        
        result = database.read("""SELECT sum(value) FROM account_operations
                                  WHERE label ='Shares'""").iloc[0]['sum(value)']
        if result is not None : return round(result,2)
        else : return 0 

        
    def get_total_recharges(self):
        
        ''' Returns the total value of the recharges '''
        
        result = database.read("""SELECT sum(value) FROM account_operations
                                  WHERE label ='Recharge'""").iloc[0]['sum(value)']
        if result is not None : return round(result,2)
        else : return 0 
        
        
        
        
    def list_account_operations_id(self):
        
        ''' Returns a tuple with all account operations IDs '''
        
        return tuple(database.read("""SELECT id FROM account_operations""")['id'])
    
#    
    
    def is_account_operation_checked(self,ID):
        
        ''' Returns True/False whether the account operation with this ID is checked or not '''
        
        assert isinstance(ID,int), "The account operation ID has to be an integer"
        assert ID in self.list_account_operations_id(), "This account operation ID does not exist"
        result = bool(database.read(f"""SELECT checked FROM account_operations
                                        WHERE id={ID}""").iloc[0]['checked'])
        return result
    
    
    
    def set_account_operation_checked(self, ID, state=True):
        
        ''' Set the checked state of the account operation with this ID, default is True '''
        
        assert isinstance(ID,int), "The account operation ID has to be an integer"
        assert ID in self.list_account_operations_id(), "This account operation ID does not exist"
        assert isinstance(state,bool), "The checked state has to be a boolean"
        
        database.write(f"""UPDATE account_operations
                           SET checked = {int(state)}
                           WHERE id={ID}""")
        
    
        
    
        
    # Caps operations
    # ==========================================================================
    
    def get_caps_balance(self):
        
        ''' Returns the global balance of the caps_operations table '''
        
        result = database.read("""SELECT sum(value) FROM caps_operations""").iloc[0]['sum(value)']
        if result is not None : return round(result,2)
        else : return 0 
    
    def get_caps_remaining(self):
        
        ''' Returns the number of remaining caps in the stock '''
       
        result = database.read("""SELECT sum(qty) FROM caps_operations""").iloc[0]['sum(qty)']
        if result is not None : return int(result)
        else : return 0 
        
    def get_caps_price(self) :
        
        ''' Returns the current caps price for users '''
        
        caps_remaining = self.get_caps_remaining()
        assert caps_remaining > 0, "There is no caps in the stock, impossible to compute the caps price. Add caps first."
        
        return round(-self.get_caps_balance()/caps_remaining,2)
        
    
    def add_caps_operation(self,label,qty,value):
        
        ''' Add a new general caps operation '''
        
        assert isinstance(label,str), "The label of this operation has to be a string"
        assert isinstance(qty,int), "The quantity of caps of this operation has to be an integer"
        assert isinstance(value,int) or isinstance(value,float), "The value of this operation has to be a number (int/float)"
        
        timestamp = get_timestamp()
        value = round(float(value),2)
        database.write(f'''INSERT INTO caps_operations (timestamp,label,qty,value)
                            VALUES ('{timestamp}','{label}',{qty},{value})''')
    
        
    def add_caps_purchase(self,qty,price):
        
        ''' Add a new caps purchase '''
        
        assert isinstance(qty,int), "The quantity of caps of this caps purchase has to be an integer"
        assert qty != 0, "The quantity of caps of this caps purchase has to be different from zero"
        assert isinstance(price,int) or isinstance(price,float), "The price of this caps purchase has to be a number (int/float)"

        self.add_caps_operation('Caps purchase',qty,-price)



    def add_supplies_purchase(self,price):
        
        ''' Records a supplies purchase '''
        
        assert isinstance(price,int) or isinstance(price,float), "The price of the supplies has to be a number (int/float)"
        assert price != 0, "The price of the supplies has to be different from zero"

        self.add_caps_operation('Supplies purchase',0,-price)
        
        
        
    def remove_missing_caps(self,qty):
        
        ''' Records a missing caps qty '''
        
        assert isinstance(qty,int), "The quantity of missing caps has to be an integer"
        assert qty != 0, "The quantity of missing caps has to be different from zero"

        self.add_caps_operation('Missing caps',-qty,0)
        
        
        
    def get_system_caps_balance(self):
        
        ''' Returns the sum of caps operations that is not associated to users'''
        
        result = database.read("""SELECT sum(value) FROM caps_operations
                                  WHERE user IS NULL """).iloc[0]['sum(value)']
        if result is not None : return round(result,2)
        else : return 0 
        
        
            
    # Donations operations
    # ==========================================================================
    
    def add_donation_operation(self,label,value):
        
        ''' Add a new donation operation '''
        
        assert isinstance(label,str), "The label of this donation operation has to be a string"
        assert isinstance(value,int) or isinstance(value,float), "The donation value has to be a number (int/float)"
        assert value != 0
        
        timestamp = get_timestamp()
        value = round(float(value),2)
        database.write(f'''INSERT INTO donation_operations (timestamp,label,value)
                            VALUES ('{timestamp}','{label}',{value})''')
            
        
    def add_charity_donation(self,donation):
        
        ''' Records a charity donation '''
        
        assert isinstance(donation,int) or isinstance(donation,float), "The donation value has to be a number (int/float)"
        assert donation != 0, "The donation value has to be different from zero"
        self.add_donation_operation('To charity',-donation)



    def get_donation_balance(self):
        
        ''' Returns the donation balance (ie what remains to be donated to a charity)'''
        
        result = database.read("""SELECT sum(value) FROM donation_operations""").iloc[0]['sum(value)']
        if result is not None : return round(result,2)
        else : return 0 
        

    def get_system_donation_balance(self):
        
        ''' Returns the sum of donation operations that is not associated to users'''
        
        result = database.read("""SELECT sum(value) FROM donation_operations
                                  WHERE user IS NULL """).iloc[0]['sum(value)']
        if result is not None : return round(result,2)
        else : return 0 
        
        
    # Balance
    # ==========================================================================
    
    def get_balance(self):
        
        ''' Returns the global balance of the system (ie what should appears in the bank account) '''
       
        # Gain : User payments in general
        user_payments = self.get_accounts_balance()
        
        # Losses : caps (+ supplies) + donation
        caps_supplies_system_balance = self.get_system_caps_balance()
        donations_system_balance = self.get_system_donation_balance()

        # Sumup
        result = user_payments + caps_supplies_system_balance + donations_system_balance
        if result is not None : return round(result,2)
        else : return 0 
        
        





                   
class User :
    
    def __init__(self,ID) :
        
        
        assert ID in System().get_user_dict().keys()
        self.ID = ID
        
        
        
        
    # Name 
    # =========================================================================
    
    def get_name(self):
        
        """ Returns user's name """
        
        result = database.read(f"""SELECT name
                                FROM users
                                WHERE id = {self.ID}""").iloc[0]['name']
        return result
        
    
    def set_name(self,name):
        
        ''' Set user's name '''
        
        assert isinstance(name,str), "The user name as to be a string"
        
        database.write(f"""UPDATE users
                           SET name = '{name}'
                           WHERE id = {self.ID}""")
        

    # Email 
    # =========================================================================

    def get_email(self):
        
        ''' Returns user's email '''
        
        result = database.read(f"""SELECT email
                                FROM users
                                WHERE id = {self.ID}""").iloc[0]['email']
        if result is None : return ''
        else: return result
    
    
    def set_email(self,email):
        
        ''' Set user's email '''
        
        assert isinstance(email,str), "The user email as to be a string"
        
        database.write(f"""UPDATE users 
                           SET email = '{email}'
                           WHERE id = {self.ID}""")
        
        

    # Tag
    # =========================================================================
    
    def set_tag(self,tag):
        
        ''' Set user's RFID tag '''
        
        assert isinstance(tag,int), "The user RFID tag as to be an integer"
        assert tag not in System().list_tags(), 'Tag %i already in use'%tag
        database.write(f"""UPDATE users
                           SET tag = {tag}
                           WHERE id = {self.ID}""")
        
    
    def get_tag(self):
        
        ''' Returns user's RFID tag '''
        
        result = database.read(f"""SELECT tag
                                   FROM users
                                   WHERE id = {self.ID}""").iloc[0]['tag']
        
        if result is not None : result = int(result)
        return result
    
    
    
    # Auto donation value
    # =========================================================================
    
    def get_auto_donation(self):
        
        ''' Returns user's auto donation '''
        
        result = database.read(f"""SELECT auto_donation
                                   FROM users
                                   WHERE id = {self.ID}""").iloc[0]['auto_donation']
        
        return round(result,2)


    def set_auto_donation(self,value):

        ''' Set user's auto donation '''
        
        assert isinstance(value,int) or isinstance(value,float), "The auto donation value has to be a number (int/float)"
        assert value>=0, "The auto donation value has to be different from zero"
        value = round(value,2)
        
        database.write(f"""UPDATE users 
                           SET auto_donation = {value}
                           WHERE id = {self.ID}""")
        
        
  
          
    # Caps conso
    # =========================================================================
    
    def add_caps_conso(self):
        
        ''' Add a caps conso for the user '''
        
        caps_price = System().get_caps_price()
        timestamp = get_timestamp()
        database.write(f'''INSERT INTO caps_operations (timestamp,label,user,qty,value)
                           VALUES ('{timestamp}', 'Conso', {self.ID}, -1, {caps_price})''')
        

    def get_total_caps_nb(self, year=None):
                
        ''' Returns the total caps qty used by the user, for the given year if provided '''
        
        assert year is None or isinstance(year,int), "The year has to be an integer"
        
        year_constraint = ''
        if year is not None :
            year = int(year)
            year_constraint = f"AND caps_operations.timestamp LIKE '{year}%' "
         
        result = database.read(f"""SELECT sum(caps_operations.qty)         
                                    FROM caps_operations
                                    INNER JOIN users       
                                    ON caps_operations.user=users.id
                                    WHERE users.id={self.ID}
                                    {year_constraint}""").iloc[0]['sum(caps_operations.qty)']
        
        if result is None or result == 0 : return 0
        else: return -result
        
        
    def get_total_caps_cost(self, year=None):
                
        ''' Returns the total caps cost paid by the user, for the given year if provided '''
        
        assert year is None or isinstance(year,int), "The year has to be an integer"
        
        year_constraint = ''
        if year is not None :
            year = int(year)
            year_constraint = f"AND caps_operations.timestamp LIKE '{year}%' "
         
        result = database.read(f"""SELECT sum(caps_operations.value)         
                                    FROM caps_operations
                                    INNER JOIN users       
                                    ON caps_operations.user=users.id
                                    WHERE users.id={self.ID}
                                    {year_constraint}""").iloc[0]['sum(caps_operations.value)']
        
        if result is None : return 0
        else: return round(result,2)    
        
        
        
        
    # Donation
    # =========================================================================
    
    def add_donation(self,label,value):
        
        ''' Add a user donation '''
        
        assert isinstance(label,str), "The donation's label as to be a string"
        assert isinstance(value,int) or isinstance(value,float), "The donation value has to be a number (int/float)"
        assert value>0, "The donation value has to be non-zero and positive"
        value = round(value,2)
        timestamp = get_timestamp()
        database.write(f'''INSERT INTO donation_operations (timestamp,label,user,value)
                           VALUES ('{timestamp}', '{label}', {self.ID}, {value})''')
        
        
    def add_manual_donation(self,value):
        
        ''' Add a user manual donation '''
        
        assert isinstance(value,int) or isinstance(value,float), "The manual donation value has to be a number (int/float)"
        assert value>0, "The donation value has to be non-zero and positive"
        self.add_donation('Manual donation',value)
        
        
    def add_auto_donation(self):
        
        ''' Add a user auto donation '''
        
        value = self.get_auto_donation()
        if value > 0 :
            self.add_donation('Auto donation',value)


    def get_total_donations(self, year=None):
        
        ''' Returns the total donation of the user '''
        
        assert year is None or isinstance(year,int), "The year has to be an integer"
        
        year_constraint = ''
        if year is not None :
            year = int(year)
            year_constraint = f"AND donation_operations.timestamp LIKE '{year}%' "
         
        result = database.read(f"""SELECT sum(donation_operations.value)          
                                    FROM donation_operations
                                    INNER JOIN users       
                                    ON donation_operations.user=users.id
                                    WHERE users.id={self.ID}
                                    {year_constraint}""").iloc[0]['sum(donation_operations.value)']
        
        if result is None : return 0
        else: return round(result,2)




    # Conso
    # =========================================================================
           
    def add_conso(self):
        
        ''' Add a new conso '''
        
        # Caps
        self.add_caps_conso()
        
        # Donation
        self.add_auto_donation()



    
    # Recharge
    # =========================================================================       
            
    def add_recharge(self,value):
        
        ''' Add a new recharge '''
        
        assert isinstance(value,int) or isinstance(value,float), "The recharge value has to be a number (int/float)"
        value = round(value,2)
        assert value != 0, "The recharge value has to be non zero"
        
        timestamp = get_timestamp()
        database.write(f'''INSERT INTO account_operations (timestamp,label,user,value)
                              VALUES ('{timestamp}','Recharge',{self.ID},{value})''')

    def get_total_recharges(self):
        
        ''' Returns total recharges value '''
        
        shares_value = database.read(f"""SELECT sum(account_operations.value)          
                                       FROM account_operations
                                       INNER JOIN users       
                                       ON account_operations.user=users.id
                                       WHERE label='Recharge'
                                       AND users.id={self.ID}""").iloc[0]['sum(account_operations.value)']
        
        if shares_value is None : return 0
        else: return round(shares_value,2)


    
    
    
    # Shares
    # =========================================================================
    
    def add_shares(self,value):
        
        ''' Add shares '''
        
        assert isinstance(value,int) or isinstance(value,float), "The recharge value has to be a number (int/float)"
        value = round(value,2)
        assert value != 0, "The recharge value has to be non zero"
        assert self.get_total_shares()+value >= 0, "The remaining shares value has to be positive"
        
        timestamp = get_timestamp()
        database.write(f'''INSERT INTO account_operations (timestamp,label,user,value)
                              VALUES ('{timestamp}','Shares',{self.ID},{value})''')
            
        
    def get_total_shares(self):
        
        ''' Returns total shares value '''
        
        shares_value = database.read(f"""SELECT sum(account_operations.value)          
                                       FROM account_operations
                                       INNER JOIN users       
                                       ON account_operations.user=users.id
                                       WHERE label='Shares'
                                       AND users.id={self.ID}""").iloc[0]['sum(account_operations.value)']
        
        if shares_value is None : return 0
        else: return round(shares_value,2)
        
        
        
        

    # All user operations 
    # =========================================================================
    
    def get_operations_by_date(self,year,month,day):
        
        ''' Returns user account informations for the given day '''
        
        assert isinstance(year,int), "The year has to be an integer"
        assert isinstance(month,int), "The month has to be an integer"
        assert isinstance(day,int), "The day has to be an integer"
        
        timestamp = dt.date(year,month,day)
        
        
        # Recharges / Shares
        df_recharges = database.read(f"""SELECT timestamp,label,value FROM account_operations
                                          INNER JOIN users       
                                          ON account_operations.user=users.id
                                          WHERE users.id={self.ID}
                                          AND date(timestamp)=date('{timestamp}')""")
        
        # Conso caps
        df_caps = database.read(f"""SELECT timestamp,label,value FROM caps_operations
                                          INNER JOIN users       
                                          ON caps_operations.user=users.id
                                          WHERE users.id={self.ID}
                                          AND date(timestamp)=date('{timestamp}')""")
        df_caps.loc[:,'value'] = - df_caps.value
        
        # Conso donation
        df_donation = database.read(f"""SELECT timestamp,label,value FROM donation_operations
                                          INNER JOIN users       
                                          ON donation_operations.user=users.id
                                          WHERE users.id={self.ID}
                                          AND date(timestamp)=date('{timestamp}')""")
        df_donation.loc[:,'value'] = - df_donation.value
        
        df = pd.concat([df_recharges,df_caps,df_donation]) 
        df.sort_values(by=['timestamp'],inplace=True)
        df.loc[:,'timestamp'] = pd.to_datetime(df.timestamp)
        df.loc[:,'timestamp'] = df.timestamp.apply( lambda x: x.strftime('%H:%M') )
        df.reset_index(drop=True,inplace=True)
    
        return df 
    
    
    

    def get_balance(self):
        
        ''' Returns the current account balance '''
        
        return round(self.get_total_recharges() - self.get_total_caps_cost() - self.get_total_donations(),2)
    
        

        

def get_current_year():
    
    ''' Returns current year '''
    
    return dt.datetime.now().year
    
    
def get_timestamp():
    
    ''' Returns current timestamp '''
    
    return dt.datetime.now().isoformat() 