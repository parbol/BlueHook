from optparse import OptionParser
import re
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patches as patches
import glob
import math


color1 = '#734C9F'
color2 = '#0198CF'
color3 = '#5DBA47'
color4 = '#F8E429'
color5 = '#FBAA4E'
color6 = '#EF4C9D'



def getMaxValues(array, index):

    if index == 1:
        maxindex = np.argmax(array[2, :])
        maxvalue = array[2, maxindex]
    elif index == 2:
        maxindex = np.argmin(array[1, :])
        maxvalue = array[1, maxindex]
    elif index == 6:
        maxvalue = array[index, array.shape[1]-1]
    else:
        maxindex = np.argmax(array[index, :])
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
    #array[5,:] /= totalPopulation


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
    fig = plt.figure(figsize = (10,15))
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



def drawFullPlot(dictionary, prob, nSeed, index, delay, tag):

    if index == 1:
        title = 'MIR'
    elif index == 2:
        title = 'MSR'
    elif index == 3:
        title = 'MRR'
    elif index == 4:
        title = 'MQR'
    elif index == 5:
        title = 'N. Tests'
    elif index == 6:
        title = 'TPR'
        

    newdir = dict()
    for k, v in dictionary.items():
        if prob not in k or delay not in k or (('engage' in k and tag not in k)):
            continue
        if 'strategy0' in k and 'asymp0.25' in k and prob in k:
           insert(newdir, k, v, 0, nSeed, index)
        elif 'strategy1' in k and 'asymp0.25' in k and 'testing100' in k and prob in k:
           insert(newdir, k, v, 1, nSeed, index)
        elif 'strategy1' in k and 'asymp0.25' in k and 'testing300' in k and prob in k:
           insert(newdir, k, v, 2, nSeed, index)
        elif 'strategy2' in k and 'asymp0.25' in k and 'testing100' in k and prob in k:
           insert(newdir, k, v, 3, nSeed, index)
        elif 'strategy2' in k and 'asymp0.25' in k and 'testing300' in k and prob in k:
           insert(newdir, k, v, 4, nSeed, index)
        elif 'strategy3' in k and 'asymp0.25' in k and 'testing100' in k and prob in k:
           insert(newdir, k, v, 5, nSeed, index)
        elif 'strategy3' in k and 'asymp0.25' in k and 'testing300' in k and prob in k:
           insert(newdir, k, v, 6, nSeed, index)
        elif 'strategy4' in k and 'asymp0.25' in k and prob in k:
           insert(newdir, k, v, 7, nSeed, index)
        elif 'strategy5' in k and 'asymp0.25' in k and 'testing100' in k and prob in k:
           insert(newdir, k, v, 8, nSeed, index)
        elif 'strategy5' in k and 'asymp0.25' in k and 'testing300' in k and prob in k:
           insert(newdir, k, v, 9, nSeed, index)
        elif 'strategy0' in k and 'asymp0.75' in k and prob in k:
           insert(newdir, k, v, 10, nSeed, index)
        elif 'strategy1' in k and 'asymp0.75' in k and 'testing100' in k and prob in k:
           insert(newdir, k, v, 11, nSeed, index)
        elif 'strategy1' in k and 'asymp0.75' in k and 'testing300' in k and prob in k:
           insert(newdir, k, v, 12, nSeed, index)
        elif 'strategy2' in k and 'asymp0.75' in k and 'testing100' in k and prob in k:
           insert(newdir, k, v, 13, nSeed, index)
        elif 'strategy2' in k and 'asymp0.75' in k and 'testing300' in k and prob in k:
           insert(newdir, k, v, 14, nSeed, index)
        elif 'strategy3' in k and 'asymp0.75' in k and 'testing100' in k and prob in k:
           insert(newdir, k, v, 15, nSeed, index)
        elif 'strategy3' in k and 'asymp0.75' in k and 'testing300' in k and prob in k:
           insert(newdir, k, v, 16, nSeed, index)
        elif 'strategy4' in k and 'asymp0.75' in k and prob in k:
           insert(newdir, k, v, 17, nSeed, index)
        elif 'strategy5' in k and 'asymp0.75' in k and 'testing100' in k and prob in k:
           insert(newdir, k, v, 18, nSeed, index)
        elif 'strategy5' in k and 'asymp0.75' in k and 'testing300' in k and prob in k:
           insert(newdir, k, v, 19, nSeed, index)

    newdirnumpy = dict()
    for k, v in newdir.items():
        newdirnumpy[k] = [np.asarray(v[0]), np.asarray(v[1])]

    plt.subplot(6, 1, index) 
    plt.figtext(0.25, 0.90, 'Asymptomatic: 25%')
    plt.figtext(0.65, 0.90, 'Asymptomatic: 75%')
    plt.ylabel(title, fontweight='bold', fontsize=10)
    plt.xlim(0, nSeed*20)
    plt.ylim(0, 1.0)
    ticks = [x for x in np.arange(nSeed*len(newdirnumpy)) if not x%5 and x %10]
    for k,v in newdirnumpy.items():
        if 'strategy0' in k:
            #color = '#051e3e'
            color = color1
            marker = '.'
            s = 7
        if 'strategy1' in k and 'testing100' in k:
            #color = '#251e3e'
            color = color2
            marker = '.'
            s = 7
        if 'strategy1' in k and 'testing300' in k:
            #color = '#251e3e'
            color = color2
            marker = 's'
            s = 5
        if 'strategy2' in k and 'testing100' in k:
            #color = '#451e3e'
            color = color3
            marker = '.'
            s = 7
        if 'strategy2' in k and 'testing300' in k:
            #color = '#451e3e'
            color = color3
            marker = 's'
            s = 5
        if 'strategy3' in k and 'testing100' in k:
            #color = '#651e3e'
            color = color4
            marker = '.'
            s = 7
        if 'strategy3' in k and 'testing300' in k:
            #color = '#651e3e'
            color = color4
            marker = 's'
            s = 5
        if 'strategy4' in k:
            #color = '#851e3e'
            color = color5
            marker = '.'
            s = 7
        if 'strategy5' in k and 'testing100' in k:
            #color = '#951e3e'
            color = color6
            marker = '.'
            s = 7
        if 'strategy5' in k and 'testing300' in k:
            #color = '#951e3e'
            color = color6
            marker = 's'
            s = 5

        if index == 5:
            plt.ylim(0, 20000)
            plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
            plt.ylabel(title, fontweight='bold', fontsize=10, labelpad=14)
        plt.plot(v[0], v[1], 'p', markersize=s, color=color, marker=marker)

    labels = ['0', '1 (100)', '1 (300)', '2 (100)', '2 (300)', '3 (100)', '3 (300)', '4', '5 (100)', '5 (300)']
    labels = labels + labels 
    for i in range(1, 20):
        plt.axvline(x=i*nSeed, color='black', linestyle='dashed')
    plt.axvline(x=10*nSeed, color='black', linestyle='solid')
    
    if index == 6:
        plt.xticks(ticks, labels, rotation=45)   
        plt.xlabel('Strategy (N. Tests)', fontweight='bold')
    else:
        plt.tick_params(axis='x', labelbottom=False)


def drawFullPlotAsymp(dictionary, asymp, nSeed, index, delay, tag):

    if index == 1:
        title = 'MIR'
    elif index == 2:
        title = 'MSR'
    elif index == 3:
        title = 'MRR'
    elif index == 4:
        title = 'MQR'
    elif index == 5:
        title = 'N. Tests'
    elif index == 6:
        title = 'TPR'
        
    plt.figtext(0.2, 0.90, 'Probability: 0.025')
    plt.figtext(0.47, 0.90, 'Probability: 0.035')
    plt.figtext(0.72, 0.90, 'Probability: 0.045')

    newdir = dict()
    for k, v in dictionary.items():
        if asymp not in k or delay not in k or (('engage' in k and tag not in k)):
            continue
        if 'strategy0' in k and 'probability0.025' in k:
           insert(newdir, k, v, 0, nSeed, index)
        elif 'strategy1' in k and 'probability0.025' in k and 'testing100' in k:
           insert(newdir, k, v, 1, nSeed, index)
        elif 'strategy1' in k and 'probability0.025' in k and 'testing300' in k:
           insert(newdir, k, v, 2, nSeed, index)
        elif 'strategy2' in k and 'probability0.025' in k and 'testing100' in k:
           insert(newdir, k, v, 3, nSeed, index)
        elif 'strategy2' in k and 'probability0.025' in k and 'testing300' in k:
           insert(newdir, k, v, 4, nSeed, index)
        elif 'strategy3' in k and 'probability0.025' in k and 'testing100' in k:
           insert(newdir, k, v, 5, nSeed, index)
        elif 'strategy3' in k and 'probability0.025' in k and 'testing300' in k:
           insert(newdir, k, v, 6, nSeed, index)
        elif 'strategy4' in k and 'probability0.025' in k:
           insert(newdir, k, v, 7, nSeed, index)
        elif 'strategy5' in k and 'probability0.025' in k and 'testing100' in k:
           insert(newdir, k, v, 8, nSeed, index)
        elif 'strategy5' in k and 'probability0.025' in k and 'testing300' in k:
           insert(newdir, k, v, 9, nSeed, index)
        elif 'strategy0' in k and 'probability0.035' in k:
           insert(newdir, k, v, 10, nSeed, index)
        elif 'strategy1' in k and 'probability0.035' in k and 'testing100' in k:
           insert(newdir, k, v, 11, nSeed, index)
        elif 'strategy1' in k and 'probability0.035' in k and 'testing300' in k:
           insert(newdir, k, v, 12, nSeed, index)
        elif 'strategy2' in k and 'probability0.035' in k and 'testing100' in k:
           insert(newdir, k, v, 13, nSeed, index)
        elif 'strategy2' in k and 'probability0.035' in k and 'testing300' in k:
           insert(newdir, k, v, 14, nSeed, index)
        elif 'strategy3' in k and 'probability0.035' in k and 'testing100' in k:
           insert(newdir, k, v, 15, nSeed, index)
        elif 'strategy3' in k and 'probability0.035' in k and 'testing300' in k:
           insert(newdir, k, v, 16, nSeed, index)
        elif 'strategy4' in k and 'probability0.035' in k:
           insert(newdir, k, v, 17, nSeed, index)
        elif 'strategy5' in k and 'probability0.035' in k and 'testing100' in k:
           insert(newdir, k, v, 18, nSeed, index)
        elif 'strategy5' in k and 'probability0.035' in k and 'testing300' in k:
           insert(newdir, k, v, 19, nSeed, index)
        elif 'strategy0' in k and 'probability0.045' in k:
           insert(newdir, k, v, 20, nSeed, index)
        elif 'strategy1' in k and 'probability0.045' in k and 'testing100' in k:
           insert(newdir, k, v, 21, nSeed, index)
        elif 'strategy1' in k and 'probability0.045' in k and 'testing300' in k:
           insert(newdir, k, v, 22, nSeed, index)
        elif 'strategy2' in k and 'probability0.045' in k and 'testing100' in k:
           insert(newdir, k, v, 23, nSeed, index)
        elif 'strategy2' in k and 'probability0.045' in k and 'testing300' in k:
           insert(newdir, k, v, 24, nSeed, index)
        elif 'strategy3' in k and 'probability0.045' in k and 'testing100' in k:
           insert(newdir, k, v, 25, nSeed, index)
        elif 'strategy3' in k and 'probability0.045' in k and 'testing300' in k:
           insert(newdir, k, v, 26, nSeed, index)
        elif 'strategy4' in k and 'probability0.045' in k:
           insert(newdir, k, v, 27, nSeed, index)
        elif 'strategy5' in k and 'probability0.045' in k and 'testing100' in k:
           insert(newdir, k, v, 28, nSeed, index)
        elif 'strategy5' in k and 'probability0.045' in k and 'testing300' in k:
           insert(newdir, k, v, 29, nSeed, index)

    newdirnumpy = dict()
    for k, v in newdir.items():
        newdirnumpy[k] = [np.asarray(v[0]), np.asarray(v[1])]

    plt.subplot(6, 1, index) 
    plt.ylabel(title, fontweight='bold', fontsize=10)
    plt.xlim(0, nSeed*30)
    plt.ylim(0, 1.0)
    ticks = [x for x in np.arange(nSeed*len(newdirnumpy)) if not x%5 and x %10]
    for k,v in newdirnumpy.items():
        if 'strategy0' in k:
            #color = '#051e3e'
            color = color1
            marker = '.'
            s = 7
        if 'strategy1' in k and 'testing100' in k:
            #color = '#251e3e'
            color = color2
            marker = '.'
            s = 7
        if 'strategy1' in k and 'testing300' in k:
            #color = '#251e3e'
            color = color2
            marker = 's'
            s = 5
        if 'strategy2' in k and 'testing100' in k:
            #color = '#451e3e'
            color = color3
            marker = '.'
            s = 7
        if 'strategy2' in k and 'testing300' in k:
            #color = '#451e3e'
            color = color3
            marker = 's'
            s = 5
        if 'strategy3' in k and 'testing100' in k:
            #color = '#651e3e'
            color = color4
            marker = '.'
            s = 7
        if 'strategy3' in k and 'testing300' in k:
            #color = '#651e3e'
            color = color4
            marker = 's'
            s = 5
        if 'strategy4' in k:
            #color = '#851e3e'
            color = color5
            marker = '.'
            s = 7
        if 'strategy5' in k and 'testing100' in k:
            #color = '#951e3e'
            color = color6
            marker = '.'
            s = 7
        if 'strategy5' in k and 'testing300' in k:
            #color = '#951e3e'
            color = color6
            marker = 's'
            s = 5

        if index == 5:
            plt.ylim(0, 20000)
            plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
            plt.ylabel(title, fontweight='bold', fontsize=10, labelpad=14)
        plt.plot(v[0], v[1], 'p', markersize=s, color=color, marker=marker)

    labels = ['0', '1 (100)', '1 (300)', '2 (100)', '2 (300)', '3 (100)', '3 (300)', '4', '5 (100)', '5 (300)']
    labels = labels + labels + labels
    for i in range(1, 30):
        plt.axvline(x=i*nSeed, color='black', linestyle='dashed')
    plt.axvline(x=10*nSeed, color='red', linestyle='solid', )
    plt.axvline(x=20*nSeed, color='red', linestyle='solid')
    
    if index == 6:
        plt.xticks(ticks, labels, rotation=45)   
        plt.xlabel('Strategy (N. Tests)', fontweight='bold')
    else:
        plt.tick_params(axis='x', labelbottom=False)



def drawFullPlotAsympDelay(dictionary, asymp, nSeed, index, prob, tag):

    if index == 1:
        title = 'MIR'
    elif index == 2:
        title = 'MSR'
    elif index == 3:
        title = 'MRR'
    elif index == 4:
        title = 'MQR'
    elif index == 5:
        title = 'N. Tests'
    elif index == 6:
        title = 'TPR'
        
    plt.figtext(0.23, 0.90, 'IPS: 0')
    plt.figtext(0.50, 0.90, 'IPS: 2')
    plt.figtext(0.76, 0.90, 'IPS: 4')

    newdir = dict()
    for k, v in dictionary.items():
        if prob not in k or asymp not in k or (('engage' in k and tag not in k)):
            continue
        if 'strategy0' in k and 'delay0' in k:
           insert(newdir, k, v, 0, nSeed, index)
        elif 'strategy1' in k and 'delay0' in k and 'testing100' in k:
           insert(newdir, k, v, 1, nSeed, index)
        elif 'strategy1' in k and 'delay0' in k and 'testing300' in k:
           insert(newdir, k, v, 2, nSeed, index)
        elif 'strategy2' in k and 'delay0' in k and 'testing100' in k:
           insert(newdir, k, v, 3, nSeed, index)
        elif 'strategy2' in k and 'delay0' in k and 'testing300' in k:
           insert(newdir, k, v, 4, nSeed, index)
        elif 'strategy3' in k and 'delay0' in k and 'testing100' in k:
           insert(newdir, k, v, 5, nSeed, index)
        elif 'strategy3' in k and 'delay0' in k and 'testing300' in k:
           insert(newdir, k, v, 6, nSeed, index)
        elif 'strategy4' in k and 'delay0' in k:
           insert(newdir, k, v, 7, nSeed, index)
        elif 'strategy5' in k and 'delay0' in k and 'testing100' in k:
           insert(newdir, k, v, 8, nSeed, index)
        elif 'strategy5' in k and 'delay0' in k and 'testing300' in k:
           insert(newdir, k, v, 9, nSeed, index)
        elif 'strategy0' in k and 'delay2' in k:
           insert(newdir, k, v, 10, nSeed, index)
        elif 'strategy1' in k and 'delay2' in k and 'testing100' in k:
           insert(newdir, k, v, 11, nSeed, index)
        elif 'strategy1' in k and 'delay2' in k and 'testing300' in k:
           insert(newdir, k, v, 12, nSeed, index)
        elif 'strategy2' in k and 'delay2' in k and 'testing100' in k:
           insert(newdir, k, v, 13, nSeed, index)
        elif 'strategy2' in k and 'delay2' in k and 'testing300' in k:
           insert(newdir, k, v, 14, nSeed, index)
        elif 'strategy3' in k and 'delay2' in k and 'testing100' in k:
           insert(newdir, k, v, 15, nSeed, index)
        elif 'strategy3' in k and 'delay2' in k and 'testing300' in k:
           insert(newdir, k, v, 16, nSeed, index)
        elif 'strategy4' in k and 'delay2' in k:
           insert(newdir, k, v, 17, nSeed, index)
        elif 'strategy5' in k and 'delay2' in k and 'testing100' in k:
           insert(newdir, k, v, 18, nSeed, index)
        elif 'strategy5' in k and 'delay2' in k and 'testing300' in k:
           insert(newdir, k, v, 19, nSeed, index)
        elif 'strategy0' in k and 'delay4' in k:
           insert(newdir, k, v, 20, nSeed, index)
        elif 'strategy1' in k and 'delay4' in k and 'testing100' in k:
           insert(newdir, k, v, 21, nSeed, index)
        elif 'strategy1' in k and 'delay4' in k and 'testing300' in k:
           insert(newdir, k, v, 22, nSeed, index)
        elif 'strategy2' in k and 'delay4' in k and 'testing100' in k:
           insert(newdir, k, v, 23, nSeed, index)
        elif 'strategy2' in k and 'delay4' in k and 'testing300' in k:
           insert(newdir, k, v, 24, nSeed, index)
        elif 'strategy3' in k and 'delay4' in k and 'testing100' in k:
           insert(newdir, k, v, 25, nSeed, index)
        elif 'strategy3' in k and 'delay4' in k and 'testing300' in k:
           insert(newdir, k, v, 26, nSeed, index)
        elif 'strategy4' in k and 'delay4' in k:
           insert(newdir, k, v, 27, nSeed, index)
        elif 'strategy5' in k and 'delay4' in k and 'testing100' in k:
           insert(newdir, k, v, 28, nSeed, index)
        elif 'strategy5' in k and 'delay4' in k and 'testing300' in k:
           insert(newdir, k, v, 29, nSeed, index)

    newdirnumpy = dict()
    for k, v in newdir.items():
        newdirnumpy[k] = [np.asarray(v[0]), np.asarray(v[1])]

    plt.subplot(6, 1, index) 
    plt.ylabel(title, fontweight='bold', fontsize=10)
    plt.xlim(0, nSeed*30)
    plt.ylim(0, 1.0)
    ticks = [x for x in np.arange(nSeed*len(newdirnumpy)) if not x%5 and x %10]
    for k,v in newdirnumpy.items():
        if 'strategy0' in k:
            #color = '#051e3e'
            color = color1
            marker = '.'
            s = 7
        if 'strategy1' in k and 'testing100' in k:
            #color = '#251e3e'
            color = color2
            marker = '.'
            s = 7
        if 'strategy1' in k and 'testing300' in k:
            #color = '#251e3e'
            color = color2
            marker = 's'
            s = 5
        if 'strategy2' in k and 'testing100' in k:
            #color = '#451e3e'
            color = color3
            marker = '.'
            s = 7
        if 'strategy2' in k and 'testing300' in k:
            #color = '#451e3e'
            color = color3
            marker = 's'
            s = 5
        if 'strategy3' in k and 'testing100' in k:
            #color = '#651e3e'
            color = color4
            marker = '.'
            s = 7
        if 'strategy3' in k and 'testing300' in k:
            #color = '#651e3e'
            color = color4
            marker = 's'
            s = 5
        if 'strategy4' in k:
            #color = '#851e3e'
            color = color5
            marker = '.'
            s = 7
        if 'strategy5' in k and 'testing100' in k:
            #color = '#951e3e'
            color = color6
            marker = '.'
            s = 7
        if 'strategy5' in k and 'testing300' in k:
            #color = '#951e3e'
            color = color6
            marker = 's'
            s = 5

        if index == 5:
            plt.ylim(0, 20000)
            plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
            plt.ylabel(title, fontweight='bold', fontsize=10, labelpad=14)
        plt.plot(v[0], v[1], 'p', markersize=s, color=color, marker=marker)

    labels = ['0', '1 (100)', '1 (300)', '2 (100)', '2 (300)', '3 (100)', '3 (300)', '4', '5 (100)', '5 (300)']
    labels = labels + labels + labels
    for i in range(1, 30):
        plt.axvline(x=i*nSeed, color='black', linestyle='dashed')
    plt.axvline(x=10*nSeed, color='red', linestyle='solid', )
    plt.axvline(x=20*nSeed, color='red', linestyle='solid')
    
    if index == 6:
        plt.xticks(ticks, labels, rotation=45)   
        plt.xlabel('Strategy (N. Tests)', fontweight='bold')
    else:
        plt.tick_params(axis='x', labelbottom=False)



def drawFullPlotBluetooth(dictionary, nSeed, index):

    if index == 1:
        title = 'MIR'
    elif index == 2:
        title = 'MSR'
    elif index == 3:
        title = 'MRR'
    elif index == 4:
        title = 'MQR'
    elif index == 5:
        title = 'N. Tests'
    elif index == 6:
        title = 'TPR'
        
    plt.figtext(0.2, 0.90, 'Engagement: 100%')
    plt.figtext(0.47, 0.90, 'Engagement: 75%')
    plt.figtext(0.72, 0.90, 'Engagement: 25%')

    newdir = dict()
    for k, v in dictionary.items():
        if 'probability0.035' not in k or 'asymp0.25' not in k or 'delay2' not in k or 'lblue4' in k:
            continue
        if 'strategy0' in k:
           insert(newdir, k, v, 0, nSeed, index)
           insert(newdir, k, v, 10, nSeed, index)
           insert(newdir, k, v, 20, nSeed, index)
        elif 'strategy1' in k and 'testing100' in k:
           insert(newdir, k, v, 1, nSeed, index)
           insert(newdir, k, v, 11, nSeed, index)
           insert(newdir, k, v, 21, nSeed, index)
        elif 'strategy1' in k and 'testing300' in k:
           insert(newdir, k, v, 2, nSeed, index)
           insert(newdir, k, v, 12, nSeed, index)
           insert(newdir, k, v, 22, nSeed, index)
        elif 'strategy2' in k and 'testing100' in k:
           insert(newdir, k, v, 3, nSeed, index)
           insert(newdir, k, v, 13, nSeed, index)
           insert(newdir, k, v, 23, nSeed, index)
        elif 'strategy2' in k and 'testing300' in k:
           insert(newdir, k, v, 4, nSeed, index)
           insert(newdir, k, v, 14, nSeed, index)
           insert(newdir, k, v, 24, nSeed, index)
        elif 'strategy3' in k and 'testing100' in k and 'engage100' in k and 'lblue2' in k:
           insert(newdir, k, v, 5, nSeed, index)
        elif 'strategy3' in k and 'testing300' in k and 'engage100' in k and 'lblue2' in k:
           insert(newdir, k, v, 6, nSeed, index)
        elif 'strategy4' in k and 'engage100' in k and 'lblue2' in k:
           insert(newdir, k, v, 7, nSeed, index)
        elif 'strategy5' in k and 'testing100' in k and 'engage100' in k and 'lblue2' in k:
           insert(newdir, k, v, 8, nSeed, index)
        elif 'strategy5' in k and 'testing300' in k and 'engage100' in k and 'lblue2' in k:
           insert(newdir, k, v, 9, nSeed, index)
        elif 'strategy3' in k and 'testing100' in k and 'engage75' in k and 'lblue2' in k:
           insert(newdir, k, v, 15, nSeed, index)
        elif 'strategy3' in k and 'testing300' in k and 'engage75' in k and 'lblue2' in k:
           insert(newdir, k, v, 16, nSeed, index)
        elif 'strategy4' in k and 'engage75' in k and 'lblue2' in k:
           insert(newdir, k, v, 17, nSeed, index)
        elif 'strategy5' in k and 'testing100' in k and 'engage75' in k and 'lblue2' in k:
           insert(newdir, k, v, 18, nSeed, index)
        elif 'strategy5' in k and 'testing300' in k and 'engage75' in k and 'lblue2' in k:
           insert(newdir, k, v, 19, nSeed, index)
        elif 'strategy3' in k and 'testing100' in k and 'engage25' in k and 'lblue2' in k:
           insert(newdir, k, v, 25, nSeed, index)
        elif 'strategy3' in k and 'testing300' in k and 'engage25' in k and 'lblue2' in k:
           insert(newdir, k, v, 26, nSeed, index)
        elif 'strategy4' in k and 'engage25' in k and 'lblue2' in k:
           insert(newdir, k, v, 27, nSeed, index)
        elif 'strategy5' in k and 'testing100' in k and 'engage25' in k and 'lblue2' in k:
           insert(newdir, k, v, 28, nSeed, index)
        elif 'strategy5' in k and 'testing300' in k and 'engage25' in k and 'lblue2' in k:
           insert(newdir, k, v, 29, nSeed, index)

    newdirnumpy = dict()
    for k, v in newdir.items():
        newdirnumpy[k] = [np.asarray(v[0]), np.asarray(v[1])]

    plt.subplot(6, 1, index) 
    plt.ylabel(title, fontweight='bold', fontsize=10)
    plt.xlim(0, nSeed*30)
    plt.ylim(0, 1.0)
    ticks = [x for x in np.arange(nSeed*30) if not x%5 and x %10]
    for k,v in newdirnumpy.items():
        if 'strategy0' in k:
            #color = '#051e3e'
            color = color1
            marker = '.'
            s = 7
        if 'strategy1' in k and 'testing100' in k:
            #color = '#251e3e'
            color = color2
            marker = '.'
            s = 7
        if 'strategy1' in k and 'testing300' in k:
            #color = '#251e3e'
            color = color2
            marker = 's'
            s = 5
        if 'strategy2' in k and 'testing100' in k:
            #color = '#451e3e'
            color = color3
            marker = '.'
            s = 7
        if 'strategy2' in k and 'testing300' in k:
            #color = '#451e3e'
            color = color3
            marker = 's'
            s = 5
        if 'strategy3' in k and 'testing100' in k:
            #color = '#651e3e'
            color = color4
            marker = '.'
            s = 7
        if 'strategy3' in k and 'testing300' in k:
            #color = '#651e3e'
            color = color4
            marker = 's'
            s = 5
        if 'strategy4' in k:
            #color = '#851e3e'
            color = color5
            marker = '.'
            s = 7
        if 'strategy5' in k and 'testing100' in k:
            #color = '#951e3e'
            color = color6
            marker = '.'
            s = 7
        if 'strategy5' in k and 'testing300' in k:
            #color = '#951e3e'
            color = color6
            marker = 's'
            s = 5

        if index == 5:
            plt.ylim(0, 20000)
            plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
            plt.ylabel(title, fontweight='bold', fontsize=10, labelpad=14)
        plt.plot(v[0], v[1], 'p', markersize=s, color=color, marker=marker)

    labels = ['0', '1 (100)', '1 (300)', '2 (100)', '2 (300)', '3 (100)', '3 (300)', '4', '5 (100)', '5 (300)']
    labels = labels + labels + labels
    for i in range(1, 30):
        plt.axvline(x=i*nSeed, color='black', linestyle='dashed')
    plt.axvline(x=10*nSeed, color='red', linestyle='solid')
    plt.axvline(x=20*nSeed, color='red', linestyle='solid')
    
    if index == 6:
        plt.xticks(ticks, labels, rotation=45)   
        plt.xlabel('Strategy (N. Tests)', fontweight='bold')
    else:
        plt.tick_params(axis='x', labelbottom=False)

def drawFullPlots(dictionary, prob, nseed, delay, tag):

    filename = prob + '_' + delay + '.png'

    fig = plt.figure(figsize = (15, 7.5))
    drawFullPlot(dictionary, prob, nseed, 1, delay, tag)
    drawFullPlot(dictionary, prob, nseed, 2, delay, tag)
    drawFullPlot(dictionary, prob, nseed, 3, delay, tag)
    drawFullPlot(dictionary, prob, nseed, 4, delay, tag)
    drawFullPlot(dictionary, prob, nseed, 5, delay, tag)
    drawFullPlot(dictionary, prob, nseed, 6, delay, tag)

    plt.savefig(filename)
    plt.close(fig)


def drawFullPlotsAsymp(dictionary, asymp, nseed, delay, tag):

    filename = asymp + '_' + delay + '.png'

    fig = plt.figure(figsize = (15, 7.5))
    drawFullPlotAsymp(dictionary, asymp, nseed, 1, delay, tag)
    drawFullPlotAsymp(dictionary, asymp, nseed, 2, delay, tag)
    drawFullPlotAsymp(dictionary, asymp, nseed, 3, delay, tag)
    drawFullPlotAsymp(dictionary, asymp, nseed, 4, delay, tag)
    drawFullPlotAsymp(dictionary, asymp, nseed, 5, delay, tag)
    drawFullPlotAsymp(dictionary, asymp, nseed, 6, delay, tag)

    plt.savefig(filename)
    plt.close(fig)

def drawFullPlotsAsympDelay(dictionary, asymp, nseed, prob, tag):

    filename = asymp + '_' + prob + '.png'

    fig = plt.figure(figsize = (15, 7.5))
    drawFullPlotAsympDelay(dictionary, asymp, nseed, 1, prob, tag)
    drawFullPlotAsympDelay(dictionary, asymp, nseed, 2, prob, tag)
    drawFullPlotAsympDelay(dictionary, asymp, nseed, 3, prob, tag)
    drawFullPlotAsympDelay(dictionary, asymp, nseed, 4, prob, tag)
    drawFullPlotAsympDelay(dictionary, asymp, nseed, 5, prob, tag)
    drawFullPlotAsympDelay(dictionary, asymp, nseed, 6, prob, tag)

    plt.savefig(filename)
    plt.close(fig)


def drawFullPlotsBluetooth(dictionary, nseed):

    filename = 'bluetooth.png'

    fig = plt.figure(figsize = (15, 7.5))
    drawFullPlotBluetooth(dictionary, nseed, 1)
    drawFullPlotBluetooth(dictionary, nseed, 2)
    drawFullPlotBluetooth(dictionary, nseed, 3)
    drawFullPlotBluetooth(dictionary, nseed, 4)
    drawFullPlotBluetooth(dictionary, nseed, 5)
    drawFullPlotBluetooth(dictionary, nseed, 6)

    plt.savefig(filename)
    plt.close(fig)



if __name__ == "__main__":


    parser = OptionParser(usage="%prog --help")
    parser.add_option("-p", "--probability",      dest="prob",        type="string",      default='-1',          help="Probability.")
    parser.add_option("-d", "--delay",            dest="delay",       type="string",      default='-1',              help="Delay.")
    parser.add_option("-a", "--asymp",            dest="asymp",       type="string",      default='-1',           help="Asymp.")
    parser.add_option("-t", "--tag",              dest="tag",         type="string",      default='engage100_lblue2',           help="Tag.")
    (options, args) = parser.parse_args()



    dictionary = readFiles()
    #draw('City_600_strategy0_probability0.025_asymp0.25\w*', dictionary, 1, 'strategy0seeds')
    #draw('City_600_strategy1_probability0.025_testing100_asymp0.25\w*', dictionary, 1, 'strategy1seeds')
    #draw('City_600_strategy2_probability0.025_testing100_asymp0.25\w*', dictionary, 1, 'strategy2seeds0.25')
    #draw('City_600_strategy2_probability0.025_testing300_asymp0.75\w*', dictionary, 1, 'strategy2seeds0.75')
    #draw('City_600_strategy3_probability0.025_testing300_engage100_lblue2_asymp0.25\w*', dictionary, 1, 'strategy3seeds')
    #draw('City_600_strategy4_probability0.025_engage100_lblue2_asymp0.25\w*', dictionary, 1, 'strategy4seeds')
    #draw('City_600_strategy5_probability0.025_testing300_engage100_lblue2_asymp0.25\w*', dictionary, 1, 'strategy5seeds')

    if options.asymp == '-1' and options.prob == '-1' and options.delay == '-1':
	    drawFullPlotsBluetooth(dictionary, 10)
    if options.asymp == '-1':
        drawFullPlots(dictionary, 'probability' + options.prob, 10, 'delay' + options.delay, options.tag)
    elif options.prob == '-1':
        drawFullPlotsAsymp(dictionary, 'asymp' + options.asymp, 10, 'delay' + options.delay, options.tag)
    elif options.delay == '-1':
        drawFullPlotsAsympDelay(dictionary, 'asymp' + options.asymp, 10, 'probability' + options.prob, options.tag)
    
