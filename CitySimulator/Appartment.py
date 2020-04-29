###############################################################
#Python-based application for handling an Appartment          #
###############################################################
import random as random

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
        self.inhabitants = []
        self.nHotPoints = 1 + int(round(random.gammavariate(conf.nHotPoints, 1)))
        self.xhot = []
        self.yhot = []
        self.lengthOfHotPoint = conf.lengthOfHotPoint
        for i in range(0, self.nHotPoints):
            self.xhot.append(random.uniform(self.x - self.lAppartment/2.0, self.x + self.lAppartment/2.0))
            self.yhot.append(random.uniform(self.y - self.lAppartment/2.0, self.y + self.lAppartment/2.0))

    def GetRandomPosition(self):

        hotpoint = random.randint(0, self.nHotPoints-1)
        while True:
            xv = random.gauss(self.xhot[hotpoint], self.lengthOfHotPoint) 
            if abs(xv - self.x) < self.lAppartment/2.0:
                break
        while True:
            yv = random.gauss(self.yhot[hotpoint], self.lengthOfHotPoint) 
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
        print('Number of persons: ' + str(self.npersons))    
        for personindex in self.persons:
            print('Person: ' + str(personindex))
        print('Number of hotpoints: ' + str(self.nHotPoints))
        for i in range(0, self.nHotPoints):
            print('HotPoint: (' + str(self.xhot[i]) + ', ' + str(self.yhot[i]) + ')')


    

