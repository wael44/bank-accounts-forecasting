# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 14:27:36 2019

@author: ASUS
"""

from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.tsa.stattools
import pylab
from client_charger import get_client ,get_client_portion
import pandas as pd

serie = get_client_portion(get_client(4),"950101",1000)
data = pd.DataFrame([serie])
data.reset_index(inplace=True)
data.index = pd.to_datetime(data.index) 
detrended = list()
o = data.values.tolist()
flat_list = [item for sublist in o for item in sublist]
o = flat_list 
for i in range(1, len(o)):
    value = o[i] - o[i-1]
    print(o[i])
    detrended.append(value)

result = seasonal_decompose(detrended, model='additive',freq=365)    


ACF = statsmodels.tsa.stattools.acf(data)
print(len(ACF))
pylab.plot( data.values.ravel(), label='original serie')
pylab.plot( result.seasonal, label='seasonality pattern')
pylab.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),fancybox=True, shadow=True, ncol=5)

pylab.show()


"""
pylab.plot( data.values.ravel(), label='original serie')
pylab.plot( result.seasonal, label='seasonality pattern')
pylab.plot( ACF, label='original serie')
pylab.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),fancybox=True, shadow=True, ncol=5)

pylab.show()

"""









"""
pylab.plot( o, label='original serie')
pylab.plot( result.seasonal, label='trend')
pylab.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)

pylab.savefig('seasonality_exemple.png', dpi=300)
pylab.show()
"""

