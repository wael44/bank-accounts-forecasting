import random
from matplotlib import pyplot as plt
from data_importer import time_series_selector

balanceList = []
for i in range(100):
    balanceList.append(random.uniform(100,150))


JUMP = 50
MIN_VALUE = 110
MIN_LENGTH = 5

def eliminate_unvailuble(list):
    list1 = list[:]
    for i in range(len(list1)):
        if list1[i] < MIN_VALUE:
            list1[i] = 0
    return list1

def best_window(indice,list):
    list1 = eliminate_unvailuble(list)
    window = []
    window.append(list1[indice])
    left_boreder = indice
    right_border =indice
    if indice < len(list1):
        for i in range(indice+1,len(list1)):
            if abs(list1[i]-min(window)) < JUMP and list1[i]!=0:
                window.append(list1[i])
                right_border = i
            else:
                right_border = i-1
                break
    if indice > 0:
        for j in range(indice-1,0,-1):
            if abs(list1[j]-min(window)) < JUMP and list1[j]!=0 :
                window.append(list1[j])
                left_boreder = j
            else:
                left_boreder = j+1
                break
    best_window = [left_boreder,right_border,min(window)]
    poids = calcul_poids(best_window)
    best_window.append(poids)
    return best_window


def all_availble_windows(list):
    windows = []
    for i in range(len(list)):
        windows.append(best_window(i,list))
    return windows

def calcul_poids(segment):
    duree = segment[1]-segment[0]+1
    valeur = segment[2]
    poids = valeur*duree*duree
    return poids


def placer_segments(serie):
    windows = all_availble_windows(serie)
    segmented_serie = []
    for k in range(len(serie)):
        segmented_serie.append(0)
     
    while len(windows )> 0:
        max_poids=0
        for i in range(len(windows)):
            if windows[i][3] > max_poids:
                max_poids = windows[i][3]
                bk = i
            else:
                bk = 0

        for j in range(windows[bk][0],windows[bk][1]):
            if  segmented_serie[j] == 0:
                segmented_serie[j] =  windows[bk][2]
        del(windows[bk])
    return segmented_serie
     
        


def main(client_id):
    serie = balanceList #time_series_selector(client_id)
#    serielist = serie.tolist()
    segmentedTS = placer_segments(serie)
    plt.plot(serie)
    plt.plot(segmentedTS)
    plt.show()

main(5)