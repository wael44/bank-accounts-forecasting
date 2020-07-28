# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 17:56:04 2019

@author: ASUS
"""

from client_charger import get_client ,get_client_portion
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import polynomial_regression_model
import decision_tree_model
import lstm_forcasting
import bayesianRidgeRegression
import randomForestRegressor
import svm_model
import arima_model
from pymongo import MongoClient

from data_preparation import accounts_importer




MaxPolReg = 0
MinPolReg = 0
MoyPolReg = []
PolRegMSE = []
MaxDecTree = 0
MinDecTree = 0
MoyTree = []
DecTreeMSE = []
MaxSvm = 0
MinSvm = 0
MoySvm = []
SvmMSE = []
MaxLstm = 0
MinLstm = 0
MoyLstm = []
LstmMSE = []
MaxBayse = 0
MinBayse = 0
MoyBayse = []
BayseMSE = []
MaxRandomForest = 0
MinRandomForest = 0
MoyRandomForest = []
RandomForestMSE = []

MaxArima = 0
MinArima = 0
MoyArima = []
ArimaMSE = []


print("start")
accounts = accounts_importer()
k=0
for i in range(1,1000):
    if i in accounts:
        print(k)
        serie = get_client_portion(get_client(i),"940105",800)
        mx,mn,mse,moy=polynomial_regression_model.main(serie)
        if mx > MaxPolReg:
            MaxPolReg = mx
        if mn > MinPolReg:
            MinPolReg = mn
        MoyPolReg.append(moy)
        PolRegMSE.append(mse)
        mx,mn,mse,moy=decision_tree_model.main(serie)
        if mx > MaxDecTree:
            MaxDecTree = mx
        if mn > MinDecTree:
            MinDecTree = mn
        MoyTree.append(moy)
        DecTreeMSE.append(mse)
        
        mx,mn,mse,moy=svm_model.main(serie)
        if mx > MaxSvm:
            MaxSvm = mx
        if mn > MinSvm:
            MinSvm = mn
        MoySvm.append(moy)
        SvmMSE.append(mse)
        
        
        mx,mn,mse,moy=lstm_forcasting.main(serie)
        if mx > MaxLstm:
            MaxLstm = mx
        if mn > MinLstm:
            MinLstm = mn
        MoyLstm.append(moy)
        LstmMSE.append(mse)
        
        mx,mn,mse,moy=bayesianRidgeRegression.main(serie)
        if mx > MaxBayse:
            MaxBayse = mx
        if mn > MinBayse:
            MinBayse = mn
        MoyBayse.append(moy)
        BayseMSE.append(mse)
        
        mx,mn,mse,moy=randomForestRegressor.main(serie)
        if mx > MaxRandomForest:
            MaxRandomForest = mx
        if mn > MinRandomForest:
            MinRandomForest = mn
        MoyRandomForest.append(moy)
        RandomForestMSE.append(mse)
        
        k += 1
        
        mx,mn,mse,moy=arima_model.main(serie)
        if mx > MaxArima:
            MaxArima = mx
        if mn > MinArima:
            MinArima = mn
        MoyArima.append(moy)
        ArimaMSE.append(mse)




MoymsePR = sum(PolRegMSE)/k
MoyPR = sum(MoyPolReg)/k
MoymseDT = sum(DecTreeMSE)/k
MoyDT = sum(MoyTree)/k

MoymseSV = sum(SvmMSE)/k
MoySV = sum(MoySvm)/k

MoymseNN = sum(LstmMSE)/k
MoyNN = sum(MoyLstm)/k

MoymseBR = sum(BayseMSE)/k
MoyBR =sum(MoyBayse)/k

MoymseRF = sum(RandomForestMSE)/k
MoyRF =sum(MoyRandomForest)/k


MoymseAM = sum(ArimaMSE)/k
MoyAM =sum(MoyArima)/k


print(float(MaxPolReg))
print(float(MaxSvm))

client = MongoClient('localhost',27017)  
col = client['pfe']['comparaison_modeles']
polynomial_regression_data = {"model": "polynomial_regression", "max_positive_error": float(MaxPolReg), 
                              "max_negative_error": float(MinPolReg),
                              "erreur_toatal_pourcentage": float(MoyPR),
                              "erreur_total_mse": float(MoymsePR)}


decision_tree_data = {"model": "decision_tree", "max_positive_error": float(MaxDecTree), 
                              "max_negative_error": float(MinDecTree),
                              "erreur_toatal_pourcentage": float(MoyDT),
                              "erreur_total_mse": float(MoymseDT)}

svm_data = {"model": "svm", "max_positive_error": float(MaxSvm), 
                              "max_negative_error": float(MinSvm),
                              "erreur_toatal_pourcentage": float(MoySV),
                              "erreur_total_mse": float(MoymseSV)}



lstm_data = {"model": "lstm", "max_positive_error": float(MaxLstm), 
                              "max_negative_error": float(MinLstm),
                              "erreur_toatal_pourcentage": float(MoyNN),
                              "erreur_total_mse": float(MoymseNN)}



bayesian_regression_data = {"model": "bayesian_regression", "max_positive_error": float(MaxBayse), 
                              "max_negative_error": float(MinBayse),
                              "erreur_toatal_pourcentage": float(MoyBR),
                              "erreur_total_mse": float(MoymseBR)}


random_forest_data = {"model": "random_forest", "max_positive_error": float(MaxRandomForest), 
                              "max_negative_error": float(MinRandomForest),
                              "erreur_toatal_pourcentage": float(MoyRF),
                              "erreur_total_mse": float(MoymseRF)}



arima_data = {"model": "arima", "max_positive_error": float(MaxArima), 
                              "max_negative_error": float(MinArima),
                              "erreur_toatal_pourcentage": float(MoyAM),
                              "erreur_total_mse": float(MoymseAM)}




data = [polynomial_regression_data,decision_tree_data,svm_data,lstm_data,bayesian_regression_data,random_forest_data,arima_data]

col.insert_many(data)


"""
plt.bar(x, height= [int(MaxPolReg),int(MaxDecTree),int(MaxSvm),int(MaxLstm),int(MaxBayse),int(MaxRandomForest)])
plt.xticks(x+.5, ['MaxPolRegError','MaxDecTreeError','MaxSvmError','MaxLstmError','MaxBayseError','MaxRandomForestError'])
plt.show()
"""
"""
f2 = plt.figure(2)
plt.bar(x, height= [float(MinPolReg),float(MinDecTree),float(MinSvm),float(MinLstm),float(MinBayse),float(MinRandomForest)])
plt.xticks(x+.5, ['MinPolRegError','MinDecTreeError','MinSvmError','MinLstmError','MinBayseError','MinRandomForestError'])
f2.show()


plt.bar(x, height= [int(MoymsePR),int(MoymseDT),int(MoymseSV),int(MoymseNN),int(MoymseBR),int(MoymseRF)])
plt.xticks(x+.5, ['MoymsePR','MoymseDT','MoymseSVM','MoymseNN','MoymseBR','MoymseRF'],rotation=90)
plt.show()


f4 = plt.figure(4)
plt.bar(x, height= [int(MoyPR),int(MoyDT),int(MoySV),int(MoyNN),int(MoyBR),int(MoyRF)])
plt.xticks(x+.5, ['MoyPRError','MoyDTError','MoySVError','MoyNNError','MoyBRError','MoyRFError'])
f4.show()
input()


"""
    
    
"""
plt.xticks(x+.5, ['1','2','3','4','5','6',
'7','8','9','10','11','12',
'13','14','15','16','17','18',
'19','20','21','22','23','24'])
"""

"""
x = np.arange(k)
fig = pyplot.figure()
ax = pyplot.subplot(111)
ax.plot(x, MaxSvm, label='maxSVM')
ax.plot(x, MinSvm, label='minSVM')
ax.plot(x, MaxPolReg, label='maxployRegression')
ax.plot(x, MinPolReg, label='minpolyregression')
ax.plot(x, MaxDecTree, label='maxdecisiontree')
ax.plot(x, MinDecTree, label='mindecisiontree')
pyplot.legend()
"""

"""  

pyplot.xlabel("number of client")
pyplot.ylabel("% d'erreur")
pyplot.show()
    
"""    
    
    
    
    



