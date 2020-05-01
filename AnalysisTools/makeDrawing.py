import pandas as pd
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import glob

def getMaxValues(f):

    array = np.genfromtxt(f, delimiter=',')
    totalPopulation = array[1, 0] + array[2, 0] + array[3, 0]
    mypopulationarray = array[2, :] / totalPopulation
    maxindex = np.argmax(mypopulationarray)
    maxvalue = mypopulationarray[maxindex]
    return [maxvalue, maxindex]

def getValues(f):

    array = np.genfromtxt(f, delimiter=',')
    return array


def makeBrazilianPlot():
    test=[]
    tag_numberoftests = ['_100']
    for tnumber in tag_numberoftests:
        for seed in range(0, 100):
            f = 'output_strategy0' + tnumber + '_seed' + str(seed) + '.csv'
            print(f)
            numpyFile=np.genfromtxt(f,delimiter=',')[2]
            if (len(numpyFile == 23)):
                test.append(numpyFile)
    df = pd.DataFrame(data=test)
    theMean=np.array([])
    theStdev=np.array([])
    for i in range(23):
        theMean=np.append(theMean,np.mean(df[i]))
        theStdev=np.append(theStdev, np.std(df[i]))
    print(theMean)
    print(theStdev)
    theDays=np.arange(23)
    plt.plot(theDays, theMean, 'k-')
    plt.fill_between(theDays, theMean-2*theStdev, theMean+2*theStdev, edgecolor='#3F7F4C', facecolor='#7EFF99',    linewidth=0)
    plt.fill_between(theDays, theMean-theStdev, theMean+theStdev, edgecolor='#1B2ACC', facecolor='#ffff00',    linewidth=0)
    plt.show()

def drawOneCase(tnumber, seed):

    filenamestrat0 = 'output_strategy0' + tnumber + '_seed' + str(seed) + '.csv' 
    filenamestrat1 = 'output_strategy1' + tnumber + '_seed' + str(seed) + '.csv' 
    array0 = getValues(filenamestrat0)
    array1 = getValues(filenamestrat1)
    plt.subplot(1, 2, 1)
    plt.plot(array0[0], array0[2], color='green')
    plt.plot(array1[0], array1[2], color='blue')
    plt.subplot(1, 2, 2)
    plt.plot(array0[0], array0[1], color='green')
    plt.plot(array1[0], array1[1], color='blue')
    plt.show()


if __name__ == "__main__":


    makeBrazilianPlot()

