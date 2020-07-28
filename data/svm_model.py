# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 17:54:45 2019

@author: ASUS
"""

from sklearn import svm
from sklearn.svm import SVR
from matplotlib import pyplot
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from client_charger import get_client ,get_client_portion
import pandas as pd 
import numpy as np
from sklearn.metrics import mean_squared_error


def splitdataset(s):
    series = s
    X = series.values
    Y = series.index.values

    day = []
    month = []
    year = []
    for y in Y:
        day.append(y.day)
        month.append(y.month)
        year.append(y.year)
    
    data = {'day': day, 'month': month, 'year': year, 'balance':X}
    df = pd.DataFrame(data)   
    
    
    X = df.loc[: ,df.columns != "balance"]
    Y = df.loc[: ,df.columns == "balance"]
    
    
    size = int(len(X) * 0.66)
    X_train, X_test = X[0:size], X[size:len(X)]
    Y_train, Y_test = Y[0:size], Y[size:len(X)]
    return X_train, X_test, Y_train, Y_test
    
    
    
def prediction(X_train , y_train , X_test):
    model = svm.SVR(kernel='poly', C=1.0 , gamma=1) 
    model.fit(X_train,y_train.values.ravel())
    y_pred= model.predict(X_test)
    return(y_pred)
    

# Function to calculate accuracy
def cal_accuracy(y_test, y_pred):
     
    print("Confusion Matrix: ",confusion_matrix(y_test, y_pred))
     
    print ("Accuracy : ",accuracy_score(y_test,y_pred)*100)
     
    print("Report :",classification_report(y_test, y_pred))




# Driver code
def main(s):
     
    X_train, X_test, y_train, y_test = splitdataset(s)
    y_pred = prediction(X_train,y_train,X_test )
    y_test = np.array(y_test.values)
    
    Max = 0
    Min = 0
    Moy = 0
    
    for i in range(len(y_test)):
        if y_test[i] > 1:
            localDiff = y_test[i]-y_pred[i]
            if localDiff < 0 and (abs(localDiff)/y_test[i]) *100 > Max:
                Max = (abs(localDiff)/y_test[i])*100
            elif localDiff > 0 and (localDiff/y_test[i]) *100 > Min:
                Min = (localDiff/y_test[i])*100
            Moy += localDiff/y_test[i]
        else:
            pass
    Moy = Moy / len(y_test)
    return y_pred,mean_squared_error(y_test, y_pred)
                

"""        
    return Max,Min,mean_squared_error(y_test, y_pred),Moy
"""    
    

