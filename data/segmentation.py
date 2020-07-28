# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 13:21:41 2019

@author: ASUS
"""
from time_series_visualizer import time_serie_plotter
from client_charger import get_client ,get_client_portion


def segment(TS1):
    JUMP = 10000 ;     # valeur pour la quelle en crée a break point
    MIN_TIME = 50;  # temps minimum en jour pour un segment non nul
    MIN_VALUE = 15000;  # valeur minimum pour un segment considéré non nul
    
    TS = TS1[:].copy()
    for i in range(len(TS)):
        balance_of_day = TS[i]
        if balance_of_day < MIN_VALUE:
            TS[i] = 0
        if i > 0 and i < len(TS)-1:
            if abs(TS[i]-TS[i-1]) <= JUMP and abs(TS[i]-TS[i+1]) <= JUMP:
                left_value = join_left(TS,i)
                right_value = join_right(TS,i,JUMP)
                if (left_value >= right_value):
                    
                    TS[i] = min(TS[i],TS[i-1])
                    
                else:
                    correct_left_side(TS,i,MIN_TIME)
                    TS[i] = min(TS[i],TS[i+1])
                    TS[i+1] = min(TS[i],TS[i+1])
                    
    return(TS)
                    
                

                    
def correct_left_side(TS,i,MIN_TIME):
    left_segment_length = -1;
    for k in range(i,0,-1):
        left_segment_length += 1
        if TS[k-1] != TS[k]:
            break
    if left_segment_length <  MIN_TIME :
        for j in range(i,0,-1):
            if TS[j] != TS[j-1]:
                bk=j-1
                new_join_value = TS[j-1]
                break
            else:
                return
        if new_join_value < TS[bk+1]:
            for z in range (i,bk,-1):
                TS[z] = new_join_value
        
            
            
        
                
                
            
            
def join_left(TS,i):
    number_of_days=1
    if i > 0:
        value = min(TS[i],TS[i-1])
        for k in range(i-1,0,-1):
            value += value
            number_of_days +=1       
            if TS[k] != TS[k-1]:
                return(value/number_of_days)
        return (value/number_of_days)
    else:
        return TS[i]
        


def join_right(TS,i,JUMP):
    number_of_days = 1
    if i < len(TS)-1:
        value = min(TS[i],TS[i+1])
        for k in range (i,len(TS)-1):
            if abs(value-TS[k]) >= JUMP:
                return(value/number_of_days)
            value += value
            number_of_days += 1
        return (value/number_of_days)
    else:
        return (TS[i])
            
            
def main():
    series = get_client_portion(get_client(1),"950105",400)
    segmented = segment(series)
    time_serie_plotter(series,segmented)
    
main()

        
