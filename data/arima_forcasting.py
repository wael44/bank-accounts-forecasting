# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 09:37:26 2019

@author: ASUS
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from client_charger import get_client ,get_client_portion
from sklearn.metrics import mean_squared_error
from data_preparation import accounts_importer


#accounts = accounts_importer()


def main(s):
    series = s
    X = series.values
    size = int(len(X) * 0.7)
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        try:
            model = ARIMA(history, order=(5,1,0))
            model_fit = model.fit(disp=0, start_ar_lags = None)
        
            output = model_fit.forecast()
            yhat = output[0]
            predictions.append(yhat)
            obs = test[t]
            history.append(obs)
        except:
            predictions.append(test[t])
#        print('predicted=%f, expected=%f' % (yhat, obs))
	

        print('predicted=%f, expected=%f' % (predictions[t], test[t]))


    error = mean_squared_error(test, predictions)
    print('Test MSE: %.3f' % error)
    
    pred = []
    temps = []
    for i in range(len(predictions)):
        pred.extend(predictions[i])
        temps.append(series.index[i])
        #############################################♥
        
    data_history = []
    data_pred = []
    data_long_period = []
    data_cash = []
    data_valuable = []
    
    data_long_period_3 = []
    data_cash_3 = []
    data_valuable_3 = []
    for i in range(len(pred)):
        data_history.append({"t": temps[i], "y": history[i]})
        data_pred.append({"t": temps[i], "y": pred[i]})








    
    print(data_history)
    print(data_pred)
        

    pyplot.plot(test)
    pyplot.plot(predictions, color='red')
    
    pyplot.show()
    print(data_history[10])
    print(data_pred[10])
    print(test[10])
    print(predictions[10])

"""
for i in range(0,10):
    if i in accounts:
"""        
main(get_client_portion(get_client(1),"960105",80))

"""
        
    predictions = np.array(predictions)
    Max = 0
    Min = 0
    for i in range(len(test)):
        localDiff = test[i]-predictions[i]
        if localDiff < 0 and (abs(localDiff)/test[i]) > Max:
            Max=(abs(localDiff)/test[i])
        elif localDiff > 0 and (localDiff/test[i]) > Min:
        	Min = (localDiff/test[i])

    return Max,Min
"""