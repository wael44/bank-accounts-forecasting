# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 10:40:25 2019

@author: ASUS
"""


import pandas as pd
from pymongo import MongoClient




def time_series_selector(indice):

    client = MongoClient('localhost',27017)

    #select database
    db = client['pfe']
    #select the collection within the database
    collection = db.balance_history_test
    #convert entire collection to Pandas dataframe
    balance = pd.DataFrame(list(collection.find()))
    del balance['_id']
    balance=balance.astype(float)
    balance = balance.iloc[: , :365]
    if (indice >= 0):
        return (balance.iloc[indice])
    else:
        return (balance.iloc[0])
    
    





    