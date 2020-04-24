###############################################################
#Python-based application for handling a Person               #
###############################################################
import numpy as np

from JanusAPI.Match import Match
from JanusAPI.User import User
from JanusAPI.JanusServer import JanusServer


class Person:

    def __init__(self, theId, person, house, floor, appartment, workplace, floorworkplace, appartmentworkplace, conf):

        self.theId = theId
        self.person = person
        #Location information  
        self.residentialBuilding = house
        self.residentialFloor = floor
        self.residentialAppartment = appartment
        self.workplaceBuilding = workplace
        self.workplaceFloor = floorworkplace
        self.workplaceAppartment = appartmentworkplace
        self.activeBuilding = house
        self.activeFloor = floor
        self.activeAppartment = appartment
        self.x = 0
        self.y = 0
        self.z = floor * 3
        #Activity times
        self.timeToGoToWork = 0 
        self.timeToLeaveWork = 0
        self.timeToGoHome = 0
        self.updateHours()

        #Last position: 0 for home, 1 for work, 2 for leisure
        self.lastposition = 0
        self.howlongcounter = 0
        self.howlong = 0
        self.leisurehowlongcounter = 0
        self.leisurehowlong = 0
        #Susceptible, Infected, Cured
        self.health = 0
        self.newHealth = 0
        self.quarantine = 0
        self.timeOfInfection = 0
        self.timeToInfect = np.random.poisson(conf.timeToInfectLambda, 1)[0]
        self.canInfect = 0
        self.timeOfIncubation = self.timeToInfect + np.random.poisson(conf.incubationLambda, 1)[0]
        self.timeOfCuration = self.timeOfIncubation + np.random.poisson(conf.curationLambda, 1)[0]
        self.symptoms = 0
        #Bluetooth 
        self.bluetoothmatches = []
        self.bluetoothOldMatches = []
        self.bluetoothUpdate = np.random.randint(0, 24*60, 1)[0]


    def updateHours(self):
        self.timeToGoToWork = np.random.normal(8, 1, 1)[0]
        self.timeToLeaveWork = np.random.normal(16, 3, 1)[0]
        self.timeToGoHome = np.random.normal(21, 3, 1)[0]


    def infect(self, time):

        self.newHealth = 1
        self.timeOfInfection = time
        self.timeToInfect = self.timeToInfect + time
        self.timeOfIncubation = self.timeOfIncubation + time
        self.timeOfCuration = self.timeOfCuration + time


    def bluetoothMatch(self, personindex, x, y, time):

        isnew = True 
        for j in self.bluetoothmatches:
            if personindex == j[0] and j[3]+1 == time:
                j[3] = time
                j[4] = j[4] + 1
                isnew = False
        if isnew:
            self.bluetoothmatches.append([personindex, x, y, time, 0])


    def updateBluetooth(self, janus):

        for i in self.bluetoothmatches:
            user1 = User(self.person, self.health, 0, self.timeOfInfection, self.timeOfCuration)
            match = Match(user1, i[0], [i[1], i[2]], i[3], i[4])
            janus.insertMatchFake(match)
            self.bluetoothOldMatches.append(i)
        self.bluetoothmatches.clear()



    def Print(self):

        print('---------------------------------------------------')
        print('|            Person  parameters                   |')
        print('---------------------------------------------------')
        print('Id: ' + self.theId)
        print('Person index: ' + str(self.person))
        print('Living in building: ' + str(self.residentialBuilding) + ', floor: ' + str(self.residentialFloor) + ', appartment: ', str(self.residentialAppartment))
        print('Working in building: ' + str(self.workplaceBuilding) + ', floor: ' + str(self.workplaceFloor) + ', appartment: ', str(self.workplaceAppartment))
        print('Active building: ' + str(self.activeBuilding) + ', floor: ' + str(self.activeFloor) + ', appartment: ', str(self.activeAppartment))
        print('Current state: ' + str(self.lastposition))
        print('Position is: (' + str(self.x) + ', ' + str(self.y) + ')')
        print('Health State is: ' + str(self.health) + ' ' + ' symptoms: ' + str(self.symptoms))
        print('Bluetoothmatches:')
        for j in self.bluetoothmatches:
            print(j)





    

