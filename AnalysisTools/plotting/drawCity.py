from optparse import OptionParser
import os
import stat
import pandas as pd
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import glob
import math

def makeOneSquare(x, y, size):

    rect = plt.Rectangle((x, y), size, size, fill=False)
    plt.gca().add_patch(rect)

def makeSubSquares(x, y, k):

    totalsize = k[0] * k[1]
    for i in range(0, k[0]):
        for j in range(0, k[0]):

            newx = x + i * k[1]
            newy = y + j * k[1] 
            makeOneSquare(newx, newy, k[1])


def makeSquares(citysize, buildingsize, streetsize, appartments):

    nbuildings = int(citysize / (buildingsize + streetsize))
    for i in range(0, nbuildings):
        for j in range(0, nbuildings):
            x = (i * (buildingsize + streetsize) + streetsize)
            y = (j * (buildingsize + streetsize) + streetsize)
            makeOneSquare(x, y, buildingsize)
            makeSubSquares(x, y, appartments[i * nbuildings + j])


def drawPeople(time, datos):

    datosInfected = []
    datosHealthy = []
    datosCured = []
    for i in datos:
        if i[0] == 0:
            datosHealthy.append(i)
        if i[0] == 1:
            datosInfected.append(i)
        if i[0] == 2:
            datosCured.append(i)

    if len(datosHealthy) != 0:
        personsHealthy = np.asmatrix(datosHealthy)
        plt.plot(personsHealthy[:, 1], personsHealthy[:, 2], '.', color='blue')
    if len(datosInfected) != 0:
        personsInfected = np.asmatrix(datosInfected)
        plt.plot(personsInfected[:, 1], personsInfected[:, 2], '.', color='red')
    if len(datosCured) != 0:
        personsCured = np.asmatrix(datosCured)
        plt.plot(personsCured[:, 1], personsCured[:, 2], '.', color='green')



if __name__ == "__main__":


    parser = OptionParser(usage="%prog --help")
    parser.add_option("-i", "--input",      dest="inputFile",         type="string",      default='citymotion.txt',          help="Name of the input file.")
    parser.add_option("-d", "--directory",  dest="dir",               type="string",      default='plots',                   help="Directory to put the plots in.")
    (options, args) = parser.parse_args()

    os.mkdir(options.dir)

    text = open(options.inputFile).readlines()
    citysize = float(text[0].split()[1])
    buildingsize = float(text[1].split()[1])
    streetsize = float(text[2].split()[1])
    population = int(text[3].split()[1])
    nhours = int((len(text) - 4)/(population+1))
    nbuildings = int(citysize/(buildingsize+streetsize))
    nbuildings = nbuildings * nbuildings
    appartments = []
    for i in range(0, nbuildings):
        v = [int(text[4+i].split()[0]), float(text[4+i].split()[1])]
        appartments.append(v)

    plt.ioff()
    for hour in range(0, nhours):
        fig = plt.figure()
        plt.xlim(0, citysize + streetsize)
        plt.ylim(0, citysize + streetsize)    
        plt.xlabel('x [m]')
        plt.ylabel('y [m]')
        a = 4 + nbuildings + hour * (population + 1)
        time = int(text[a])
        theday = int(time/(24*60))
        thehour = int(math.floor((time - theday * 24 * 60) / 60.0))
        theminute = int(time - theday * 24 * 60 - thehour * 60)
        plt.title('City at Day: ' + str(theday) + ' Hour: ' + str(thehour) + ' Minute: ' + str(theminute))
        personxy = []
        for i in range(0, population):
            inf = float(text[a+i+1].split()[0])
            x = float(text[a+i+1].split()[1])
            y = float(text[a+i+1].split()[2])
            vect = []
            vect.append(inf)
            vect.append(x)
            vect.append(y)
            personxy.append(vect)

        drawPeople(time, personxy)
        makeSquares(citysize, buildingsize, streetsize, appartments)
        #plt.show()
        plt.savefig(options.dir + '/city_' + str(time) + '.png')
        plt.close(fig)






