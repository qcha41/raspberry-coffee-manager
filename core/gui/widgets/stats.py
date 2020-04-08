# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 08:58:14 2020

@author: qchat
"""

import datetime as dt

class StatsPanel:
    
    def __init__(self,gui):
        
        self.gui = gui
        
        # Connect signals
        self.gui.stats_return_pushButton.clicked.connect(self.return_pressed)
        
        # Return countdown
        self.callback_countdown_update = lambda x : self.gui.stats_return_pushButton.setText(f'Return\n({x})')
        self.callback_countdown_end = self.return_pressed
        
        
    def start(self):
        
        ''' Initialize panel '''
        
        # Load current user
        self.user = self.gui.current_user
        
        # Load all opearations
        operations = self.user.get_all_operations()
        operations.loc[:,'timestamp'] = operations.timestamp.apply( lambda x: x.date() )
        operations.loc[:,'year'] = operations.timestamp.apply( lambda x: x.year )
        operations.loc[:,'month'] = operations.timestamp.apply( lambda x: x.month )
        operations.loc[:,'week_number'] = operations.timestamp.apply( lambda x: x.isoformat()[1] )
        operations.loc[:,'day'] = operations.timestamp.apply( lambda x: x.day )
        
        
        # Display user infos
        self.gui.stats_name_label.setText(self.user.get_name())
        
        # First operation date
        if len(operations)>0 :
            first_date = operations[operations.timestamp == min(operations.timestamp)].iloc[0].timestamp.strftime('%d/%m/%Y')
            self.gui.stats_firstDate_label.setText(first_date)
        else : 
            self.gui.stats_firstDate_label.setText('New user')
        
        # Update current dates
        today = dt.date.today()
        self.gui.stats_curryear_label.setText('('+str(today.year)+')')
        self.gui.stats_currmonth_label.setText('('+today.strftime('%B')+')')
        self.gui.stats_currweek_label.setText('('+today.strftime('%W')+')')
        self.gui.stats_currday_label.setText('('+today.strftime('%A')+')')
        
        # Display statistics
        self.display_statistics(operations,'allTime')
        operations = operations.loc[operations.year == today.year]
        self.display_statistics(operations,'thisYear')
        operations = operations.loc[operations.month == today.month]
        self.display_statistics(operations,'thisMonth')
        operations = operations.loc[operations.week_number == today.isoformat()[1]]
        self.display_statistics(operations,'thisWeek')
        operations = operations.loc[operations.day == today.day]
        self.display_statistics(operations,'today')
        
        # Balance
        self.gui.stats_balance_label.setText(f'{self.user.get_balance()} \u20ac')
        
        # Return button
        self.gui.countdown.start()
        
    
    def display_statistics(self,operations,period):
        
        # Nb_caps
        nb_caps = len(operations.loc[operations.label=='Conso'])
        getattr(self.gui,f'stats_nbCaps_{period}_label').setText(str(nb_caps))
        
        # Recharge
        recharges = round(sum(operations.loc[operations.label=='Recharge','value']),2)
        getattr(self.gui,f'stats_recharges_{period}_label').setText(str(recharges)+' \u20ac')
        
        # Caps
        consos = round(sum(operations.loc[operations.label=='Conso','value']),2)
        getattr(self.gui,f'stats_consos_{period}_label').setText(str(consos)+' \u20ac')
        
        # Donation
        donations = round(sum(operations.loc[operations.label.str.contains('donation'),'value']),2)
        getattr(self.gui,f'stats_donations_{period}_label').setText(str(donations)+' \u20ac')
        
        
        
    def stop (self):
        
        ''' Uninitialize panel '''
        
        pass
    
    
    
    # Return
    # =========================================================================
    
    def return_pressed(self):
        
        ''' Open account panel '''
        
        self.gui.switch_panel_signal.emit('account') 
        