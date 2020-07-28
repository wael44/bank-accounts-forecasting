# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 12:17:36 2019

@author: ASUS
"""


from client_charger import get_client ,get_client_portion
from segmentation import segment
import polynomial_regression_model
import decision_tree_model
import svm_model
import lstm_forcasting
import arima_model
import bayesianRidgeRegression
import randomForestRegressor
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





accounts = accounts_importer()
k=0
for i in range(1,1000):
    if i in accounts:
        print(k)
        seriex = get_client_portion(get_client(i),"940105",800)
        serie = segment(seriex)
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
        
        mx,mn,mse,moy=arima_model.main(serie)
        if mx > MaxArima:
            MaxArima = mx
        if mn > MinArima:
            MinArima = mn
        MoyArima.append(moy)
        ArimaMSE.append(mse)
        
        
        k += 1




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




client = MongoClient('localhost',27017)  
col = client['pfe']['comparaison_modeles_avec_segmentation']
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

