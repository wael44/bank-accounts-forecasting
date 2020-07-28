# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 15:53:35 2019

@author: ASUS
"""

from data_preparation import date_populater,accounts_importer
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import datetime


def get_client(id):
    date = date_populater()
 #○   accounts = accounts_importer()
    client = MongoClient('localhost',27017)  
    col = client['pfe']['balance_history']
    df = pd.DataFrame(list(col.find({"account_id": id})))
    balance = []
    
    for i in range (len(date)):
        balance.append(0)
        
    balance_history = pd.Series(balance, index=date)
    for i in range(len(df["balance"])):
        d = df["date"]
        balance_history[d] = df["balance"]
        
    for i in range(1,len(balance_history)):
        if balance_history.iloc[i] ==0.0:
            balance_history[i] = balance_history[i-1]
            
            
    return(balance_history)
    
def get_client_for_regression(id):
    client = MongoClient('localhost',27017) 
    col1 = client['pfe']['clients']
    col2 = client['pfe']['demographic_data']
    col3 = client['pfe']['relation_disposition']
    col4 = client['pfe']['account']
    
    balance = get_client(id)    
    accounts = accounts_importer()
    
    BD = pd.DataFrame(balance)
    BD = BD.transpose()
    BD["account_id"]=id
    
    account_data = list(col4.find({"account_id": id}))
    relation_data = list(col3.find({"account_id": id, "type": 'OWNER'}))
    client_data = list(col1.find({"client_id": relation_data[0]["client_id"]}))
    BD["client_id"]= relation_data[0]["client_id"]
    BD["branch_location"] = account_data[0]["district_id"]
    BD["account_date_creation"] = account_data[0]["date"]
    BD["client_birth"] = client_data[0]["birth_number"]
    discret = client_data[0]["district_id"]
    demographic_data = list(col2.find({"A1": discret}))  
    BD["no. of inhabitants"] = demographic_data[0]["A4"]
    BD["no. of municipalities with inhabitants < 499"] = demographic_data[0]["A5"]
    BD["no. of municipalities with inhabitants 500-1999"] = demographic_data[0]["A6"]
    BD["no. of municipalities with inhabitants 2000-9999"] = demographic_data[0]["A7"]
    BD["no. of municipalities with inhabitants >10000"] = demographic_data[0]["A8"]
    BD["no. of cities"] = demographic_data[0]["A9"]
    BD["ratio of urban inhabitants"] = demographic_data[0]["A10"]
    BD["average salary"] = demographic_data[0]["A11"]
    BD["unemploymant rate 95"] = demographic_data[0]["A12"]
    BD["unemploymant rate 96"] = demographic_data[0]["A13"]
    BD["no. of enterpreneurs per 1000 inhabitants"] = demographic_data[0]["A14"]
    BD["no. of commited crimes 95"] = demographic_data[0]["A15"]
    BD["no. of commited crimes 96"] = demographic_data[0]["A16"]
    
    for i in accounts:
    
    
    
    
        BD1 = get_client(i)
        BD1 = BD1.transpose()
        BD1["account_id"]=i
    
        account_data = list(col4.find({"account_id": i}))
        relation_data = list(col3.find({"account_id": i, "type": 'OWNER'}))
        client_data = list(col1.find({"client_id": relation_data[0]["client_id"]}))
        BD1["client_id"]= relation_data[0]["client_id"]
        BD1["branch_location"] = account_data[0]["district_id"]
        BD1["account_date_creation"] = account_data[0]["date"]
        BD1["client_birth"] = client_data[0]["birth_number"]
        discret = client_data[0]["district_id"]
        demographic_data = list(col2.find({"A1": discret}))  
        BD1["no. of inhabitants"] = demographic_data[0]["A4"]
        BD1["no. of municipalities with inhabitants < 499"] = demographic_data[0]["A5"]
        BD1["no. of municipalities with inhabitants 500-1999"] = demographic_data[0]["A6"]
        BD1["no. of municipalities with inhabitants 2000-9999"] = demographic_data[0]["A7"]
        BD1["no. of municipalities with inhabitants >10000"] = demographic_data[0]["A8"]
        BD1["no. of cities"] = demographic_data[0]["A9"]
        BD1["ratio of urban inhabitants"] = demographic_data[0]["A10"]
        BD1["average salary"] = demographic_data[0]["A11"]
        BD1["unemploymant rate 95"] = demographic_data[0]["A12"]
        BD1["unemploymant rate 96"] = demographic_data[0]["A13"]
        BD1["no. of enterpreneurs per 1000 inhabitants"] = demographic_data[0]["A14"]
        BD1["no. of commited crimes 95"] = demographic_data[0]["A15"]
        BD1["no. of commited crimes 96"] = demographic_data[0]["A16"]
        BD = BD.append(BD1,ignore_index=True)
    
    print(BD)
 

    
        
    
    
"""
    plt.plot(balance_history)
    plt.show()
    print(balance_history)
"""    
    
def get_client_portion(client_history,date_debut,nbre_de_jour):

    date_debut = datetime.datetime.strptime(date_debut, "%y%m%d")
    end_date = date_debut + datetime.timedelta(days=nbre_de_jour)
    date_debut = date_debut.date()
    end_date = end_date.date()
    
    balance_history = client_history[date_debut:end_date]
    return balance_history
    
"""    
    plt.plot(balance_history)
    plt.show()
    get_client_portion(get_client(1),"950105",700)
    
"""    

            
            
        
        
        
        
    
    
