# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 10:57:24 2019

@author: ASUS
"""
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
import time
from pymongo import MongoClient

"""
def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta
def date_populater():
    days = []
    for result in perdelta(date(1993, 1, 1), date(1998, 12, 20), timedelta(days=1)):
        days.append(result)
    return(days)
 
    
        
def accounts_importer():
    with open('trans2.csv','r') as csv_file:
        lines = csv_file.readlines()
    accounts = []
    for line in lines:
        data = line.split(';')
        accounts.append(data[1])
    del accounts[0]
    finalAccounts=[]
    for i in accounts:
        if i not in finalAccounts:
            finalAccounts.append(i)
    finalAccounts = list(map(int, finalAccounts))
    return(finalAccounts)
"""



def transfrom_time(datx):
#    return datetime.strptime(date, '%y%m%d').date()
    return pd.to_datetime(datx,format='%y%m%d')



def data_frame_populater():

    df = pd.read_csv('trans.csv',sep=";")
    
    df=df[["account_id","date","balance","amount","type"]]
    
    df["date"]=df["date"].iloc[:].apply(lambda x: transfrom_time(str(x)))
    print(df)
    
    
    client = MongoClient('localhost',27017)  
    col = client['pfe']['relation_transaction']
    data = df.to_dict(orient='records')  
    col.insert_many(data)

data_frame_populater()




"""
        
            
    
    
    
data_frame_populater()



def data_frame_populater():

    df = pd.read_csv('loan.csv',sep=";")
    

    
    print(df)
    

    client = MongoClient('localhost',27017)  
    col = client['pfe']['loan']
    data = df.to_dict(orient='records')  
    col.insert_many(data)

data_frame_populater()
"""