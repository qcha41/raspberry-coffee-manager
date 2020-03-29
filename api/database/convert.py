# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 15:42:51 2020

@author: qchat
"""

from interface import Database
import os 
import numpy as np
import pandas as pd


 
def reset_and_convert_old_version(oldDBpath,newDBpath):
    
    # Prepare and handle database
    try : 
        os.remove(newDBpath)
    except : pass
    oldDtb = Database(oldDBpath)
    newDtb = Database(newDBpath)
    newDtb.auto_commit = False
    users_old = oldDtb.read('SELECT * FROM Users')
    consos_old = oldDtb.read('SELECT * FROM UserOperations')
    donations_old = oldDtb.read('SELECT * FROM Donations')
    operations_old = oldDtb.read('SELECT * FROM SystemOperations')
    operations_old.rename(columns={'description':'label'},inplace=True)

    
    # In-situ modifications of old databases
    users_old.rename(columns={'donation':'auto_donation'},inplace=True)
    d = {1:'Caps',2:'Donation',3:'Recharge'}
    consos_old.rename(columns={'item':'label'},inplace=True)
    consos_old.loc[:,'label'] = consos_old.label.apply(lambda x: d[x])
    
    
    
    # Users
    # -------------------------------------------------------------------------
    users = users_old
    users.loc[:,'tag'] = users.tag.astype('Int64')
    users.loc[:,'name'] = "'"+users.name+"'"
    users.loc[:,'email'] = "'"+users.email+"'"
    
    
    
    # account_operations
    # -------------------------------------------------------------------------
    account_operations = consos_old.loc[consos_old.label=='Recharge']
    account_operations.loc[:,'timestamp'] = "'"+account_operations.timestamp+"'"
    account_operations.loc[:,'label'] = "'"+account_operations.label+"'"
    account_operations.loc[:,'checked'] = 1

    # caps_operations
    # -------------------------------------------------------------------------
    
    # Add caps conso
    caps_operations_temp1 = consos_old.loc[consos_old.label=='Caps']
    caps_operations_temp1.loc[:,'value'] = - caps_operations_temp1.value
    caps_operations_temp1.loc[:,'label'] = 'Conso'
    caps_operations_temp1.loc[:,'qty'] = -1
    caps_operations_temp1.drop(columns=['id'],inplace=True)

    # Add caps added to the stock
    caps_operations_temp2 = operations_old
    caps_operations_temp2.rename(columns={"caps": "qty"},inplace=True)
    caps_operations_temp2.drop(columns=['id'],inplace=True)
    caps_operations_temp2.loc[(caps_operations_temp2.label=='Supplies')|(caps_operations_temp2.label=='Sugar')|(caps_operations_temp2.label=='Descaling')|(caps_operations_temp2.label=='Descaling-sugar'),'label'] = 'Supplies purchase'
    caps_operations_temp2.loc[(caps_operations_temp2.label=='Caps')|(caps_operations_temp2.label=='Backup conso V2'), 'label' ] = 'Caps purchase'
    caps_operations_temp2.loc[caps_operations_temp2.label=='Missing-caps', 'label' ] = 'Missing caps'
    
    # Uniformization
    caps_operations = pd.concat([caps_operations_temp1,caps_operations_temp2],sort=True)
    caps_operations.loc[:,'user'] = caps_operations.user.astype('Int64')
    caps_operations.sort_values(by=['timestamp'],inplace=True)
    caps_operations.loc[:,'timestamp'] = "'"+caps_operations.timestamp+"'"
    caps_operations.loc[:,'label'] = "'"+caps_operations.label+"'"

    # donation_operations
    # -------------------------------------------------------------------------
    
    # Add user donation
    donation_operations_temp1 = consos_old.loc[consos_old.label=='Donation']
    donation_operations_temp1.loc[:,'value'] = - donation_operations_temp1.value
    donation_operations_temp1.loc[:,'label'] = 'Auto donation'
    donation_operations_temp1.drop(columns=['id'],inplace=True)
    
    
    # Add system donation    
    donation_operations_temp2 = donations_old
    donation_operations_temp2.loc[:,'value'] = - donation_operations_temp2.value
    donation_operations_temp2.loc[:,'label'] = 'To charity'
    donation_operations_temp2.drop(columns=['id'],inplace=True)

    # Merge
    donation_operations = pd.concat([donation_operations_temp1,donation_operations_temp2],sort=True)
    donation_operations.sort_values(by=['timestamp'],inplace=True)
    donation_operations.loc[:,'user'] = donation_operations.user.astype('Int64')
    donation_operations.loc[:,'timestamp'] = "'"+donation_operations.timestamp+"'"
    donation_operations.loc[:,'label'] = "'"+donation_operations.label+"'"
    

    # Saving to new database
    # -------------------------------------------------------------------------
    for i in range(len(users)) :
        user = users.iloc[i]
        if np.isnan(user.tag) : user.tag = 'NULL'
        if not isinstance(user.email,str) : user.email = 'NULL'
        newDtb.write(f"""INSERT INTO users (id,name,tag,email,auto_donation) 
                         VALUES ({user.id},{user["name"]},{user.tag},{user.email},{user.auto_donation}) """)
        
    for i in range(len(account_operations)) :
        op = account_operations.iloc[i]
        newDtb.write(f"""INSERT INTO account_operations (timestamp,label,user,value,checked) 
                         VALUES ({op.timestamp},{op.label},{op.user},{op.value},{op.checked}) """)
    
    for i in range(len(caps_operations)) :
        op = caps_operations.iloc[i]
        if np.isnan(op.user) : op.user = 'NULL'
        newDtb.write(f"""INSERT INTO caps_operations (timestamp,label,user,qty,value) 
                         VALUES ({op.timestamp},{op.label},{op.user},{op.qty},{op.value}) """)
   
    for i in range(len(donation_operations)) :
        op = donation_operations.iloc[i]
        if np.isnan(op.user) : op.user = 'NULL'
        newDtb.write(f"""INSERT INTO donation_operations (timestamp,label,user,value) 
                         VALUES ({op.timestamp},{op.label},{op.user},{op.value}) """)
   
    newDtb.commit()
#    
    # Close databases
    # -------------------------------------------------------------------------
    oldDtb.close()
    newDtb.close()
    

reset_and_convert_old_version(r'C:\Users\qchat\Documents\GitHub\data\database_old.db',
                              r'C:\Users\qchat\Documents\GitHub\data\database.db')
