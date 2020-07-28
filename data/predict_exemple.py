# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 21:07:25 2019

@author: ASUS
"""

import svm_model
import arima_model
from pymongo import MongoClient
import pylab
from client_charger import get_client ,get_client_portion

serie = get_client_portion(get_client(4),"950105",800)
svm_prediction,rmse_svm=svm_model.main(serie)
test,arima_prediction,rmse_arima=arima_model.main(serie)

flat_list = [item for sublist in arima_prediction.tolist() for item in sublist]
arima_prediction =  flat_list
svm_prediction = svm_prediction.tolist()
"""
pyplot.plot(test)
pyplot.plot(svm_prediction, color='red')
pyplot.show()
"""


pylab.plot( test, label='true value')
pylab.plot( svm_prediction, label='svm_prediction')
pylab.plot( arima_prediction,  label='arima_prediction')
pylab.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
pylab.savefig('svm_arima_3.png', dpi=300)
#pylab.show()





"""
client = MongoClient('localhost',27017)  
col = client['pfe']['predictions']
serie = {"serie": serie.values.tolist(), "svm_prediction": svm_prediction.tolist(), 
                              "arima_prediction": arima_prediction,
                              "rmse_svm": rmse_svm,
                              "rmse_arima": rmse_arima}




col.insert_one(serie)

"""












"""
error = mean_squared_error(test, predictions)
print('Test MSE: %.3f' % error)


pyplot.plot(test)
pyplot.plot(predictions, color='red')

pyplot.show()
"""

"""
def splitdataset(se):
    series = se
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
    
    
    size = int(len(X) * 0.7)
    X_train, X_test = X[0:size], X[size:len(X)]
    Y_train, Y_test = Y[0:size], Y[size:len(X)]
    return X_train, X_test, Y_train, Y_test
    
    
    
def prediction(X_train , y_train , X_test):
    model = svm.SVR(kernel='poly', C=1.0 , gamma=1) 
    model.fit(X_train,y_train.values.ravel())
    y_pred= model.predict(X_test)
    return(y_pred)
    




# Driver code
def main(s):
    
    X_train, X_test, y_train, y_test = splitdataset(s)
    y_pred = prediction(X_train,y_train,X_test )
    y_test = np.array(y_test.values)
    for i in range(len(y_test)):
        print('predicted=%f, expected=%f' % (y_pred[i], y_test[i]))
    pyplot.plot(y_test)
    pyplot.plot(y_pred, color='red')

    pyplot.show()
    
main(s)
    
"""