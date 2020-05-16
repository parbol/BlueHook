import re
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patches as patches
import glob
import math


def getMaxValues(array, index):

    if index != 1:
        maxindex = np.argmax(array[index, :])
    else:
        maxindex = np.argmin(array[index, :])
    maxvalue = array[index, maxindex]
    return maxvalue


def normalize(array):

    totalPopulation = array[1, 0] + array[2, 0] + array[3, 0]
    array[1,:] /= totalPopulation
    array[2,:] /= totalPopulation
    array[3,:] /= totalPopulation
    array[4,:] /= totalPopulation
    for j in range(0, array.shape[1]): 
        if array[5, j] != 0:
            array[6,j] /= array[5,j]
    array[5,:] /= totalPopulation


def readFiles():

    myDict = dict()
    a = os.getcwd()
    for i in os.listdir():
        if 'City' in i and 'strategy' in i:
            for j in os.listdir(i):
                if '.csv' in j:
                    array = np.genfromtxt(i + '/' + j, delimiter=',')
                    normalize(array)
                    name = j[j.find('City'):j.find('.csv')]
                    myDict[name] = array
    return myDict				



def drawOneCase(array):

    plt.subplot(2, 3, 1)
    plt.plot(array[0], array[2], color='green')
    plt.subplot(2, 3, 2)
    plt.plot(array[0], array[1], color='green')
    plt.subplot(2, 3, 3)
    plt.plot(array[0], array[3], color='green')
    plt.subplot(2, 3, 4)
    plt.plot(array[0], array[4], color='green')
    plt.subplot(2, 3, 5)
    plt.plot(array[0], array[5], color='green')
    plt.subplot(2, 3, 6)
    plt.plot(array[0], array[6], color='green')


def draw(text, dictionary, yaxis, name):

    listOfArrays = []
    regex = re.compile(text)
    for k, v in dictionary.items():
        if regex.match(k):
            maxvalue = getMaxValues(v, 2)
            if maxvalue < 0.001:
                print('In ', k, ' the epidemic was stopped')
            else:
                listOfArrays.append(v)

    maxIndex = listOfArrays[0].shape[1]
    fig = plt.figure(figsize = (10,10))
    plt.subplot(2, 3, 1)
    plt.title('Fraction of infected')
    plt.xlim(0, listOfArrays[0][0][maxIndex-1])
    plt.ylim(0, yaxis)
    plt.subplot(2, 3, 2)
    plt.title('Fraction of susceptible')
    plt.xlim(0, listOfArrays[0][0][maxIndex-1])
    plt.ylim(0, yaxis)
    plt.subplot(2, 3, 3)
    plt.title('Fraction of cured')
    plt.xlim(0, listOfArrays[0][0][maxIndex-1])
    plt.ylim(0, yaxis)
    plt.subplot(2, 3, 4)
    plt.title('Fraction of quarantined')
    plt.xlim(0, listOfArrays[0][0][maxIndex-1])
    plt.ylim(0, yaxis)
    plt.subplot(2, 3, 5)
    plt.title('Number of tests')
    plt.xlim(0, listOfArrays[0][0][maxIndex-1])
    plt.ylim(0, yaxis)
    plt.subplot(2, 3, 6)
    plt.title('Fraction of positive tests')
    plt.xlim(0, listOfArrays[0][0][maxIndex-1])
    plt.ylim(0, yaxis)

    for i in listOfArrays:
        drawOneCase(i)

    plt.savefig(name + '.png')
    plt.close(fig)



def insert(newdir, k, v, offset, nSeed, index):
    

    name = k[0:k.find('_seed')]
    seedpos = int(k[k.find('CitySeed')+8:len(k)])
    maxvalue = getMaxValues(v, index)
    print('Entering in', k, maxvalue)
    if name in newdir.keys():
        newdir[name][0].append(offset * nSeed + seedpos)
        newdir[name][1].append(maxvalue)
    else:
        seedvector = []
        yvector = []
        seedvector.append(offset * nSeed + seedpos)
        yvector.append(maxvalue)
        vector = [seedvector, yvector]
        newdir[name] = vector



def drawFullPlot(dictionary, prob, nSeed, index):

    if index == 1:
        title = 'Susceptibles [%]'
    elif index == 2:
        title = 'Infected [%]'
    elif index == 3:
        title = 'Recovered [%]'
    elif index == 4:
        title = 'Quarantine [%]'
    elif index == 5:
        title = 'Tests [%]'
    elif index == 6:
        title = 'Positive tests [%]'
        

    newdir = dict()
    for k, v in dictionary.items():
        if 'strategy0' in k and 'asymp0.25' in k and prob in k:
           insert(newdir, k, v, 0, nSeed, index)
        elif 'strategy1' in k and 'asymp0.25' in k and 'testing50' in k and prob in k:
           insert(newdir, k, v, 1, nSeed, index)
        elif 'strategy1' in k and 'asymp0.25' in k and 'testing100' in k and prob in k:
           insert(newdir, k, v, 2, nSeed, index)
        elif 'strategy2' in k and 'asymp0.25' in k and 'testing50' in k and prob in k:
           insert(newdir, k, v, 3, nSeed, index)
        elif 'strategy2' in k and 'asymp0.25' in k and 'testing100' in k and prob in k:
           insert(newdir, k, v, 4, nSeed, index)
        elif 'strategy3' in k and 'asymp0.25' in k and 'testing50' in k and prob in k:
           insert(newdir, k, v, 5, nSeed, index)
        elif 'strategy3' in k and 'asymp0.25' in k and 'testing100' in k and prob in k:
           insert(newdir, k, v, 6, nSeed, index)
        elif 'strategy4' in k and 'asymp0.25' in k and prob in k:
           insert(newdir, k, v, 7, nSeed, index)
        elif 'strategy5' in k and 'asymp0.25' in k and 'testing50' in k and prob in k:
           insert(newdir, k, v, 8, nSeed, index)
        elif 'strategy5' in k and 'asymp0.25' in k and 'testing100' in k and prob in k:
           insert(newdir, k, v, 9, nSeed, index)
        elif 'strategy0' in k and 'asymp0.75' in k and prob in k:
           insert(newdir, k, v, 10, nSeed, index)
        elif 'strategy1' in k and 'asymp0.75' in k and 'testing50' in k and prob in k:
           insert(newdir, k, v, 11, nSeed, index)
        elif 'strategy1' in k and 'asymp0.75' in k and 'testing100' in k and prob in k:
           insert(newdir, k, v, 12, nSeed, index)
        elif 'strategy2' in k and 'asymp0.75' in k and 'testing50' in k and prob in k:
           insert(newdir, k, v, 13, nSeed, index)
        elif 'strategy2' in k and 'asymp0.75' in k and 'testing100' in k and prob in k:
           insert(newdir, k, v, 14, nSeed, index)
        elif 'strategy3' in k and 'asymp0.75' in k and 'testing50' in k and prob in k:
           insert(newdir, k, v, 15, nSeed, index)
        elif 'strategy3' in k and 'asymp0.75' in k and 'testing100' in k and prob in k:
           insert(newdir, k, v, 16, nSeed, index)
        elif 'strategy4' in k and 'asymp0.75' in k and prob in k:
           insert(newdir, k, v, 17, nSeed, index)
        elif 'strategy5' in k and 'asymp0.75' in k and 'testing50' in k and prob in k:
           insert(newdir, k, v, 18, nSeed, index)
        elif 'strategy5' in k and 'asymp0.75' in k and 'testing100' in k and prob in k:
           insert(newdir, k, v, 19, nSeed, index)

    newdirnumpy = dict()
    for k, v in newdir.items():
        newdirnumpy[k] = [np.asarray(v[0]), np.asarray(v[1])]

    plt.subplot(6, 1, index) 
    plt.figtext(0.25, 0.90, 'Asymptomatic: 25%')
    plt.figtext(0.65, 0.90, 'Asymptomatic: 75%')
    plt.ylabel(title, fontweight='bold')
    plt.xlim(0, nSeed*20)
    plt.ylim(0, 1.0)
    ticks = [x for x in np.arange(nSeed*len(newdirnumpy)) if not x%5 and x %10]
    for k,v in newdirnumpy.items():
        plt.plot(v[0], v[1], 'p')

    labels = ['0', '1 (50)', '1 (100)', '2 (50)', '2 (100)', '3 (50)', '3 (100)', '4', '5 (50)', '5 (100)']
    labels = labels + labels
    for i in range(1, 20):
        plt.axvline(x=i*nSeed, color='black', linestyle='dashed')
    plt.axvline(x=10*nSeed, color='black', linestyle='solid')
    
    if index == 6:
        plt.xticks(ticks, labels, rotation=45)   
        plt.xlabel('Strategy (N. Tests)', fontweight='bold')
    else:
        plt.tick_params(axis='x', labelbottom=False)

def drawFullPlots(dictionary, prob, nseed):

    fig = plt.figure(figsize = (15, 15))
    drawFullPlot(dictionary, prob, nseed, 1)
    drawFullPlot(dictionary, prob, nseed, 2)
    drawFullPlot(dictionary, prob, nseed, 3)
    drawFullPlot(dictionary, prob, nseed, 4)
    drawFullPlot(dictionary, prob, nseed, 5)
    drawFullPlot(dictionary, prob, nseed, 6)
    plt.show() 

if __name__ == "__main__":

    dictionary = readFiles()
    #draw('City_600_strategy0_probability0.025_asymp0.25\w*', dictionary, 1, 'strategy0seeds')
    #draw('City_600_strategy1_probability0.025_testing50_asymp0.25\w*', dictionary, 1, 'strategy1seeds')
    #draw('City_600_strategy2_probability0.025_testing50_asymp0.25\w*', dictionary, 1, 'strategy2seeds0.25')
    #draw('City_600_strategy2_probability0.025_testing100_asymp0.75\w*', dictionary, 1, 'strategy2seeds0.75')
    #draw('City_600_strategy3_probability0.025_testing100_engage100_lblue2_asymp0.25\w*', dictionary, 1, 'strategy3seeds')
    #draw('City_600_strategy4_probability0.025_engage100_lblue2_asymp0.25\w*', dictionary, 1, 'strategy4seeds')
    #draw('City_600_strategy5_probability0.025_testing100_engage100_lblue2_asymp0.25\w*', dictionary, 1, 'strategy5seeds')
    drawFullPlots(dictionary, 'probability0.025', 10)

