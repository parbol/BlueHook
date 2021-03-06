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

def makeDiffHistogram(dir0, dir1):
    #parser = OptionParser(usage="%prog --help")
    #(options, args) = parser.parse_args()
    diffMaxl = []
    diffDayl = []

    tag_numberoftests = ['_100']
    for tnumber in tag_numberoftests:
        for seed in range(0, 50):
            filenamestrat0 = dir0 + '/output_' + dir0 + '_seed' + str(seed) + '.csv' 
            filenamestrat1 = dir1 + '/output_' + dir1 + '_seed' + str(seed) + '.csv' 
            val0 = getMaxValues(filenamestrat0) 
            val1 = getMaxValues(filenamestrat1) 
            diffMax = val0[0] - val1[0]
            diffDay = val0[1] - val1[1]
            diffMaxl.append(diffMax)
            diffDayl.append(diffDay)
    maxl = np.asarray(diffMaxl)
    dayl = np.asarray(diffDayl)

    plt.subplot(1,2,1)
    plt.hist(maxl, bins=20, range=(-0.1, 0.1))
    plt.axvline(maxl.mean(), color='k')
    plt.subplot(1,2,2)
    plt.hist(dayl, bins=10, range=(-10, 10))
    plt.axvline(dayl.mean(), color='k')
    plt.show()


def makeBrazilianPlot(folder):
    listInfected=[]
    tag_numberoftests = ['_100']
    for tnumber in tag_numberoftests:
        for seed in range(0, 50):
            f= folder + '/output_' + folder + '_seed' + str(seed) + '.csv'
            numpyInfected=np.genfromtxt(f,delimiter=',')[2]
            nCitizens=np.genfromtxt(f,delimiter=',')[1][0]+1
            numpyInfected=100*numpyInfected/nCitizens
            listInfected.append(numpyInfected)
    df = pd.DataFrame(data=listInfected)
    theMean=np.array([])
    theStdev=np.array([])
    theDays=np.arange(len(numpyInfected))
    for i in theDays:
        theMean=np.append(theMean,np.mean(df[i]))
        theStdev=np.append(theStdev, np.std(df[i]))
    plt.plot(theDays, theMean, 'k-')
    #plt.fill_between(theDays, theMean-2*theStdev, theMean+2*theStdev, edgecolor='#3F7F4C', facecolor='#7EFF99',    linewidth=0, alpha=0.5)
    plt.fill_between(theDays, theMean-theStdev, theMean+theStdev, edgecolor='#1B2ACC', facecolor='#ffff00',    linewidth=0, alpha=0.5)
    plt.xlabel("Days")
    plt.ylabel("% of infected people")
    plt.title(folder)
    plt.show()
    plt.savefig('foo.png')

def drawOneCase(dir0, dir1, seed):

    filenamestrat0 = dir0 + '/output_' + dir0 + '_seed' + str(seed) + '.csv' 
    filenamestrat1 = dir1 + '/output_' + dir1 + '_seed' + str(seed) + '.csv' 
    array0 = getValues(filenamestrat0)
    array1 = getValues(filenamestrat1)
    plt.subplot(2, 2, 1)
    plt.plot(array0[0], array0[2], color='green')
    plt.plot(array1[0], array1[2], color='blue')
    plt.subplot(2, 2, 2)
    plt.plot(array0[0], array0[1], color='green')
    plt.plot(array1[0], array1[1], color='blue')
    plt.subplot(2, 2, 3)
    plt.plot(array0[0], array0[3], color='green')
    plt.plot(array1[0], array1[3], color='blue')
    plt.subplot(2, 2, 4)
    plt.plot(array0[0], array0[4], color='green')
    plt.plot(array1[0], array1[4], color='blue')
    plt.show()


if __name__ == "__main__":


#    makeDiffHistogram('CitySize500_Strategy1_Testing100', 'CitySize500_Strategy3_Testing100')
    
#drawOneCase('CitySize500_Strategy0_Testing50', 'CitySize500_Strategy3_Testing50', 0)
    makeBrazilianPlot('CitySize500_Strategy1_Testing100')
