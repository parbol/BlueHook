###############################################################
#Python-based application for handling a Person               #
###############################################################
import numpy as np

from JanusAPI.Match import Match
from JanusAPI.User import User
from JanusAPI.JanusServer import JanusServer


class Person:

    def __init__(self, theId, person, house, floor, appartment, workplace, floorworkplace, appartmentworkplace):

        self.theId = theId
        self.person = person
        self.residentialBuilding = house
        self.residentialFloor = floor
        self.residentialAppartment = appartment
        self.workplaceBuilding = workplace
        self.workplaceFloor = floorworkplace
        self.workplaceAppartment = appartmentworkplace
        self.activeBuilding = house
        self.activeFloor = floor
        self.activeAppartment = appartment
        #Susceptible, Infected, Cured
        self.health = 0
        self.newHealth = 0
        self.timeOfInfection = 0
        self.timeOfCuration = 0
        self.timeOfIncubation = 0
        self.timeInfected = 0
        self.symptoms = 0
        #Last position: 0 for home, 1 for work, 2 for leisure
        self.lastposition = 0
        self.x = 0
        self.y = 0
        self.z = floor * 3
        self.howlongcounter = 0
        self.howlong = 0
        self.leisurehowlongcounter = 0
        self.leisurehowlong = 0
        self.bluetoothmatches = []
        self.bluetootholdmatches = []
        self.bluetoothUpdate = np.random.randint(0, 24*60, 1)[0]

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
            
    def __init__(self, nameid, state, firstlogin, infectiondate, curationdate):


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





    

