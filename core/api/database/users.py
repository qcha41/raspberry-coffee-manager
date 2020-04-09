# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 20:37:52 2020

@author: qchat
"""


from . import system
from .main import database
from . import utilities

import datetime as dt
import pandas as pd


                   
class User :
    
    def __init__(self,ID) :
        
        assert ID in system.get_user_dict().keys()
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
        
        assert isinstance(name,str), "The user namehas to be a string"
        
        database.write(f"""UPDATE users
                           SET name = '{name}'
                           WHERE id = {self.ID}""")
        
        
    # Active
    # =========================================================================
        
    def is_active(self):
        
        """ Returns user's active state """
        
        result = database.read(f"""SELECT active
                                FROM users
                                WHERE id = {self.ID}""").iloc[0]['active']
        return bool(result)
        
    
    def set_active(self,state):
        
        ''' Set user's active state '''
        
        assert isinstance(state,bool), "The user active state has to be a boolean"
        
        database.write(f"""UPDATE users
                           SET active = {int(state)}
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
        
        assert isinstance(email,str), "The user emailhas to be a string"
        
        database.write(f"""UPDATE users 
                           SET email = '{email}'
                           WHERE id = {self.ID}""")
        
        

    # Tag
    # =========================================================================
    
    def set_tag(self,tag):
        
        ''' Set user's RFID tag '''
        
        assert isinstance(tag,int), "The user RFID taghas to be an integer"
        assert tag not in system.list_tags(), 'Tag %i already in use'%tag
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
        
        caps_price = system.get_caps_price()
        if caps_price is not None :
            timestamp = utilities.get_timestamp()
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
        
        assert isinstance(label,str), "The donation's labelhas to be a string"
        assert isinstance(value,int) or isinstance(value,float), "The donation value has to be a number (int/float)"
        assert value>0, "The donation value has to be non-zero and positive"
        value = round(value,2)
        timestamp = utilities.get_timestamp()
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
        
        timestamp = utilities.get_timestamp()
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
        
        timestamp = utilities.get_timestamp()
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
    
    
    def get_all_operations(self):
        
        # Recharges / Shares
        df_recharges = database.read(f"""SELECT timestamp,label,value FROM account_operations
                                          INNER JOIN users       
                                          ON account_operations.user=users.id
                                          WHERE users.id={self.ID}""")
        
        # Conso caps
        df_caps = database.read(f"""SELECT timestamp,label,value FROM caps_operations
                                          INNER JOIN users       
                                          ON caps_operations.user=users.id
                                          WHERE users.id={self.ID}""")
        df_caps.loc[:,'value'] = - df_caps.value
        
        # Conso donation
        df_donation = database.read(f"""SELECT timestamp,label,value FROM donation_operations
                                          INNER JOIN users       
                                          ON donation_operations.user=users.id
                                          WHERE users.id={self.ID}""")
        df_donation.loc[:,'value'] = - df_donation.value
    
        df = pd.concat([df_recharges,df_caps,df_donation]) 
        df.sort_values(by=['timestamp'],inplace=True)
        df.loc[:,'timestamp'] = pd.to_datetime(df.timestamp)
        df.reset_index(drop=True,inplace=True)
        
        return df
    

    def get_balance(self):
        
        ''' Returns the current account balance '''
        
        return round(self.get_total_recharges() - self.get_total_caps_cost() - self.get_total_donations(),2)
    