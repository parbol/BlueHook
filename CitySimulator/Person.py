###############################################################
#Python-based application for handling a Person               #
###############################################################
import numpy as np

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
        self.timeToGoToWork = 1441 
        self.timeToLeaveWork = 1441
        self.timeToGoHome = 1441
        self.oldTimeToGoHome = 1441 
        self.setHours()

        #Last position: 0 for home, 1 for work, 2 for leisure
        self.lastposition = 0
        self.howlongcounter = 0
        self.howlong = 0
        self.leisurehowlongcounter = 0
        self.leisurehowlong = 0
        #Susceptible, Infected, Cured, Tested
        self.health = 0
        self.newHealth = 0
        self.quarantine = 0
        self.timeOfInfection = 0
        self.timeToInfect = np.random.poisson(conf.timeToInfectLambda, 1)[0]
        self.canInfect = 0
        self.timeOfIncubation = self.timeToInfect + np.random.poisson(conf.incubationLambda, 1)[0]
        self.timeOfCuration = self.timeOfIncubation + np.random.poisson(conf.curationLambda, 1)[0]
        dice = np.random.uniform(0, 1, 1)[0]
        if dice < conf.noSymptomsProbability:
            self.hasSymptoms = 0
        else:
            self.hasSymptoms = 1
        self.symptoms = 0
        self.tested = 0
        #Bluetooth 
        self.bluetoothmatches = []
        self.bluetoothOldMatches = []
        self.bluetoothUpdate = np.random.randint(0, 24*60, 1)[0]

    def setHours(self):
        self.oldTimeToGoHome = self.timeToGoHome
        while True:
            self.timeToGoToWork = int(np.random.normal(480, 60, 1)[0]) 
            if self.timeToGoToWork < 240 or self.timeToGoToWork > 660:
                continue
            self.timeToLeaveWork = (self.timeToGoToWork + int(np.random.normal(480, 60, 1)[0]))
            self.timeToGoHome = (self.timeToLeaveWork + int(np.random.normal(240, 120, 1)[0]))
            if self.timeToGoHome >= 1440:
                continue

            break

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
            janus.insertMatch('person_' + str(self.person), 'person_' + str(i[0]), int(self.health), int(0), int(self.timeOfInfection), int(self.timeOfCuration), i[1], i[2], int(i[3]), int(i[4]))
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
        print('Time to go home: ', str(self.timeToGoHome))
        print('Time to go work: ', str(self.timeToGoToWork))
        print('Time to leave work: ', str(self.timeToLeaveWork))
        print('Current state: ' + str(self.lastposition))
        print('Position is: (' + str(self.x) + ', ' + str(self.y) + ')')
        print('Health State is: ' + str(self.health) + ' can infect is: ' + str(self.canInfect))
        print('Tested State is: ' + str(self.tested))
        print('Can have symptoms: ' + str(self.hasSymptoms) + ', has symptoms: ' + str(self.symptoms))
        print('Quarentine is: ' + str(self.quarantine))
        print('Time of infection: ' + str(self.timeOfInfection))
        print('Time to infect: ' + str(self.timeToInfect))
        print('Time of incubation: ' + str(self.timeOfIncubation))
        print('Time of curation: ' + str(self.timeOfCuration))

        print('Bluetoothmatches:')
        for j in self.bluetoothmatches:
            print(j)





    

