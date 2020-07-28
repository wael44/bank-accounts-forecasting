# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 21:16:10 2019

@author: ASUS
"""

from statsmodels.tsa.arima_model import ARIMA
import numpy as np
from sklearn.metrics import mean_squared_error





def main(s):
    series = s
    X = series.values
    size = int(len(X) * 0.66)
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
            
            
    Max = 0
    Min = 0
    Moy = 0
    predictions = np.array(predictions)
    
    
    for i in range(len(test)):
        if test[i] > 1:
            localDiff = test[i]-predictions[i]
            if localDiff < 0 and (abs(localDiff)/test[i])*100 > Max:
                Max = (abs(localDiff)/test[i])*100
            elif localDiff > 0 and (localDiff/test[i])*100 > Min:
                Min = (localDiff/test[i])*100
            Moy += localDiff/test[i]
        else:
            pass
    Moy = Moy / len(test)
    return test,predictions,mean_squared_error(test, predictions)
"""

    return Max,Min,mean_squared_error(test, predictions),Moy
    
"""    