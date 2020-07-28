# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 13:48:06 2019

@author: ASUS
"""

import pandas as pd
from datetime import date, timedelta, datetime
import time
from pymongo import MongoClient


def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta
def date_populater():
    days = []
    for result in perdelta(date(1993, 1, 1), date(1998, 12, 20), timedelta(days=1)):
        days.append(result);
    return(days);
    
    
        
        
        
def accounts_importer():
    with open('trans.csv','r') as csv_file:
        lines = csv_file.readlines()
    accounts = [];
    for line in lines:
        data = line.split(';')
        accounts.append(data[1])
    del accounts[0]
    finalAccounts=[];
    for i in accounts:
        if i not in finalAccounts:
            finalAccounts.append(i)
    return(finalAccounts)
        
 



def data_frame_initielizer():
    
    
    accounts = accounts_importer()
    days = date_populater()
    zero_init =[]
    for i in range(len(accounts)):
        zero_init.append(0)
    
    data = {}
    
    for k in days:
        data[k]=zero_init
        
    df = pd.DataFrame(data,index=accounts)
    return(df)




def data_frame_populater():
    
    
    start = time.time()
    
    df = data_frame_initielizer()
    accounts_id = []
    dates = []
    balance = []
    initdates = []
    with open('trans.csv','r') as csv_file:
        lines = csv_file.readlines()
    for line in lines:
        data = line.split(';')
        accounts_id.append(data[1])
        initdates.append(data[2])
        balance.append(data[6])
    del initdates[0]
    del balance[0]
    del accounts_id[0]
    
    for i in initdates:
        dates.append(datetime.strptime(i, '%y%m%d').date())
        
    # populate the dataframe with true values from history of transactions
    print(len(dates))
    for i, d in enumerate(dates):
        b = balance[i]
        c = accounts_id[i]
        df.loc[c,d] = b
        
        
    # populate the rest of the dataframe with recent values for zeros members
    
    
    
    for j in range(1,len(df.columns)):
        if (df.iloc[1,j]==0):
            df.iloc[1,j]=df.iloc[1,j-1]
    
    
    
    
    
    
    #populating MongoDB
    
    
    client = MongoClient('localhost',27017)  # Remember your uri string
    col = client['pfe']['balance_history_test']
    df.columns = df.columns.astype(str)
    data = df.to_dict(orient='records')  # Here's our added param..
    col.insert_many(data)
        
        
            
    
    
    
    
        
    end = time.time()
    print (end-start , "  : seconds ")    
    print("-----------------------------------------")     
    print ("Done with success")  
    print(df)

    

data_frame_populater()