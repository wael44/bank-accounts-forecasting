# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 13:11:49 2019

@author: ASUS
"""

from client_charger import get_client ,get_client_portion
import pandas as pd 

series = get_client_portion(get_client(1),"950105",700)

X = series.values
Y = series.index.values

day = []
month = []
year = []
i= 0
for y in Y:
    day.append(y.day)
    month.append(y.month)
    year.append(y.year)
    
data = {'day': day, 'month': month, 'year': year, 'balance':X}
df = pd.DataFrame(data) 
  