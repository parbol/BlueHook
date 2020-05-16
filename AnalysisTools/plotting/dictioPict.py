import re
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patches as patches
import glob
import math


def getMaxValues(array):

    maxindex = np.argmax(array[2, :])
    maxvalue = array[2, maxindex]
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
            if getMaxValues(v) < 0.001:
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


if __name__ == "__main__":

    dictionary = readFiles()
    draw('City_600_strategy0_probability0.025_asymp0.25\w*', dictionary, 1, 'strategy0seeds')
    draw('City_600_strategy1_probability0.025_testing100_asymp0.25\w*', dictionary, 1, 'strategy1seeds')
    draw('City_600_strategy2_probability0.025_testing100_asymp0.25\w*', dictionary, 1, 'strategy2seeds')
    draw('City_600_strategy3_probability0.025_testing100_engage100_lblue2_asymp0.25\w*', dictionary, 1, 'strategy3seeds')
    draw('City_600_strategy4_probability0.025_engage100_lblue2_asymp0.25\w*', dictionary, 1, 'strategy4seeds')
    draw('City_600_strategy5_probability0.025_testing100_engage100_lblue2_asymp0.25\w*', dictionary, 1, 'strategy5seeds')

