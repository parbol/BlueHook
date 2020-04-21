###############################################################
#Python-based application for handling an Appartment          #
###############################################################
import numpy as np


class Appartment:

    def __init__(self, buildingId, floorId, appId, conf, x, y, lAppartment):

        self.building = buildingId
        self.floor = floorId
        self.appartment = appId
        self.x = x
        self.y = y
        self.lAppartment = lAppartment
        self.persons = []
        self.npersons = 0
        self.nHotPoints = 1 + np.random.poisson(conf.nHotPoints, 1)[0]
        self.xhot = []
        self.yhot = []
        self.lengthOfHotPoint = conf.lengthOfHotPoint
        for i in range(0, self.nHotPoints):
            self.xhot.append(np.random.uniform(self.x - self.lAppartment/2.0, self.x + self.lAppartment/2.0, 1)[0])
            self.yhot.append(np.random.uniform(self.y - self.lAppartment/2.0, self.y + self.lAppartment/2.0, 1)[0])

    def GetRandomPosition(self):

        hotpoint = np.random.randint(0, self.nHotPoints)
        while True:
            xv = np.random.normal(self.xhot[hotpoint], self.lengthOfHotPoint) 
            if abs(xv - self.x) < self.lAppartment/2.0:
                break
        while True:
            yv = np.random.normal(self.yhot[hotpoint], self.lengthOfHotPoint) 
            if abs(yv - self.y) < self.lAppartment/2.0:
                break
        return [xv, yv]

    def assignPeople(self, people):

        self.persons = people
        self.npersons = len(people)
 
    def addPerson(self, personindex):

        if personindex not in self.persons:
            self.persons.append(personindex)

    def removePerson(self, personindex):

        if personindex in self.persons:
            self.persons.remove(personindex)
       
    def Print(self):

        print('---------------------------------------------------')
        print('|             Apparment parameters                 |')
        print('---------------------------------------------------')
        print('Building Id: ' + str(self.building))
        print('Floor Id: ' + str(self.floor))
        print('Appartment Id: ' + str(self.appartment))
        print('Location: (' + str(self.x) + ', ' + str(self.y) + ')')
        print('Size of Appartments: ' + str(self.lAppartment))
        print('Number of hotpoints: ' + str(self.nHotPoints))
        print('Number of persons: ' + str(self.npersons))    
        for personindex in self.persons:
            print('Person: ' + str(personindex))


    

