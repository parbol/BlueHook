###############################################################
#Python-based application for handling a city                 #
###############################################################
import numpy as np
import math

from CitySimulator.Building import Building
from CitySimulator.Person import Person



class City:

    def __init__(self, size, lBuilding, lStreet, population, fracRes, fracWor, fracLei, nFloorIndex, nAppartmentIndex):
 
        #Internal parameters of the city
        self.size = size
        self.lBuilding = lBuilding
        self.lStreet = lStreet
        self.lBlock = (lBuilding + lStreet)
        self.nIter = int(size / self.lBlock)
        self.population = population
        self.fracRes = fracRes
        self.fracWor = fracWor
        self.fracLei = fracLei
        self.nFloorIndex = nFloorIndex
        self.nAppartmentIndex = nAppartmentIndex
        self.timescalehome = 120
        self.timescalework = 30
        self.timescaleleisure = 30
        self.leisurescale = 3
        self.leisuresitescale = 40

        #Creating the places of the city
        listOfBuildings = self.BuildingBuilder()
 
        self.listOfResidentialBuildings = listOfBuildings[0][0]
        self.nResidentialPlaces = len(listOfBuildings[0][0])
        self.nAppartmentResidentialPlaces = listOfBuildings[0][1]
        self.averagePopulationPerAppartment = int(self.population / self.nAppartmentResidentialPlaces)

        self.listOfWorkBuildings = listOfBuildings[1][0]
        self.nWorkPlaces = len(listOfBuildings[1][0])
        self.nAppartmentWorkPlaces = listOfBuildings[1][1]
    
        self.listOfLeisureBuildings = listOfBuildings[2][0]
        self.nLeisurePlaces = len(listOfBuildings[2][0])
        self.nAppartmentLeisurePlaces = listOfBuildings[2][1]
        
        #Creating the population
        self.thePopulation = self.PopulationBuilder()
        self.realPopulation = len(self.thePopulation)

    ###################################################################################################
    ###################################################################################################
    def getHour(self, time):

        days = math.floor(time / (24.0*60.0))
        newtime = time - days * 24
        hour = math.floor(newtime / 60)
        return hour

    ###################################################################################################
    ###################################################################################################
    def run(self, time):

        hour = self.getHour(time) 

        for person in self.thePopulation:
            if (hour >= 0 and hour < 8) or (hour > 21 and hour < 24):
                if person.lastposition != 0:
                    self.goHome(person)
                else:
                    self.runHome(person)
            elif (hour >= 8 and hour < 16):
                if person.lastposition != 1:
                    self.goWork(person)
                else:
                    self.runWork(person)
            else:
                if person.lastposition != 2:
                    self.goLeisure(person)
                else:
                    self.runLeisure(person)

    ###################################################################################################
    ###################################################################################################
    def goHome(self, person):
        
        person.lastposition = 0
        [person.x, person.y] = self.listOfResidentialBuildings[person.building].floors[person.floor].appartments[person.appartment].GetRandomPosition()
        person.howlongcounter = 0
        person.howlong = np.random.poisson(self.timescalehome, 1)[0]

    ###################################################################################################
    ###################################################################################################
    def runHome(self, person):

        person.howlongcounter = person.howlongcounter + 1
        if person.howlongcounter >= person.howlong:
            [person.x, person.y] = self.listOfResidentialBuildings[person.building].floors[person.floor].appartments[person.appartment].GetRandomPosition()
            person.howlongcounter = 0
            person.howlong = np.random.poisson(self.timescalehome, 1)[0]

    ###################################################################################################
    ###################################################################################################
    def goWork(self, person):

        person.lastposition = 1
        [person.x, person.y] = self.listOfWorkBuildings[person.workplace].floors[person.floorWorkplace].appartments[person.appartmentWorkplace].GetRandomPosition()
        person.howlongcounter = 0
        person.howlong = np.random.poisson(self.timescalework, 1)[0]

    ###################################################################################################
    ###################################################################################################
    def runWork(self, person):

        person.howlongcounter = person.howlongcounter + 1
        if person.howlongcounter >= person.howlong:
            [person.x, person.y] = self.listOfWorkBuildings[person.workplace].floors[person.floorWorkplace].appartments[person.appartmentWorkplace].GetRandomPosition()
            self.howlongcounter = 0
            self.howlong = np.random.poisson(self.timescalework, 1)[0]

    ###################################################################################################
    ###################################################################################################
    def goLeisure(self, person):

        person.lastposition = 2
        person.leisurehowlong = np.random.poisson(self.leisuresitescale, 1)[0]
        person.leisurehowlongcounter = 0 
        person.leisurePlace = np.random.randint(0, self.nLeisurePlaces, 1)[0]
        person.floorLeisurePlace = 0
        person.appartmentLeisurePlace = np.random.randint(0, self.listOfLeisureBuildings[person.leisurePlace].floors[0].nAppartments, 1)[0]
        [person.x, person.y] = self.listOfLeisureBuildings[person.leisurePlace].floors[0].appartments[person.appartmentLeisurePlace].GetRandomPosition()
        person.howlongcounter = 0
        person.howlong = np.random.poisson(self.leisurescale, 1)[0]

    ###################################################################################################
    ###################################################################################################
    def runLeisure(self, person):
        
        person.howlongcounter = person.howlongcounter + 1
        person.leisurehowlongcounter = person.leisurehowlongcounter + 1
        if person.leisurehowlongcounter >= person.leisurehowlong:
            person.leisurehowlong = np.random.poisson(self.leisuresitescale, 1)[0]
            person.leisurehowlongcounter = 0 
            person.leisurePlace = np.random.randint(0, self.nLeisurePlaces, 1)[0]
            person.floorLeisurePlace = 0
            person.appartmentLeisurePlace = np.random.randint(0, self.listOfLeisureBuildings[person.leisurePlace].floors[0].nAppartments, 1)[0]
            [person.x, person.y] = self.listOfLeisureBuildings[person.leisurePlace].floors[0].appartments[person.appartmentLeisurePlace].GetRandomPosition()
            person.howlongcounter = 0
            person.howlong = np.random.poisson(self.leisurescale, 1)[0]
 
        if person.howlongcounter >= person.howlong:
            [person.x, person.y] = self.listOfLeisureBuildings[person.leisurePlace].floors[0].appartments[person.appartmentLeisurePlace].GetRandomPosition()
            person.howlongcounter = 0
            person.howlong = np.random.poisson(self.leisurescale, 1)[0]
        
    ###################################################################################################
    ###################################################################################################
    def BuildingBuilder(self):

        buildingsResidential = []
        buildingsWork = []
        buildingsLeisure = []
        nAppartmentResidential = 0
        nAppartmentWork = 0
        nAppartmentLeisure = 0

        buildingresidential = 0
        buildingwork = 0
        buildingleisure = 0
        for i in range(0, self.nIter):
            for j in range(0, self.nIter):
                #Type of building  
                dice = np.random.uniform(0, 1, 1)
                if dice < self.fracRes:
                    thefloors = 1 + np.random.poisson(self.nFloorIndex, 1)[0]
                    theappartments = 1 + np.random.poisson(self.nAppartmentIndex, 1)[0]
                    nAppartmentResidential = nAppartmentResidential + (theappartments * thefloors)
                    thebuilding = Building(buildingresidential, self.lBuilding, i * self.lBlock + self.lStreet + self.lBuilding/2.0, j * self.lBlock + self.lStreet + self.lBuilding/2.0, 0, thefloors, theappartments)
                    buildingsResidential.append(thebuilding)
                    buildingresidential = buildingresidential + 1
                elif dice >= self.fracRes and dice < (self.fracWor + self.fracRes):
                    thefloors = 1 + np.random.poisson(self.nFloorIndex, 1)[0]
                    theappartments = 1 + np.random.poisson(self.nAppartmentIndex, 1)[0]
                    nAppartmentWork = nAppartmentWork + theappartments * thefloors
                    thebuilding = Building(buildingwork, self.lBuilding, i * self.lBlock + self.lStreet + self.lBuilding/2.0, j * self.lBlock + self.lStreet + self.lBuilding/2.0, 1, thefloors, theappartments)
                    buildingsWork.append(thebuilding)
                    buildingwork = buildingwork + 1
                else:
                    thefloors = 1 
                    theappartments = 1 + np.random.poisson(self.nAppartmentIndex, 1)[0]
                    nAppartmentLeisure = nAppartmentLeisure + theappartments * thefloors
                    thebuilding = Building(buildingleisure, self.lBuilding, i * self.lBlock + self.lStreet + self.lBuilding/2.0, j * self.lBlock + self.lStreet + self.lBuilding/2.0, 2, thefloors, theappartments)
                    buildingsLeisure.append(thebuilding)
                    buildingleisure = buildingleisure + 1
        return [[buildingsResidential, nAppartmentResidential], [buildingsWork, nAppartmentWork], [buildingsLeisure, nAppartmentLeisure]]
   
   
    ###################################################################################################
    ###################################################################################################
    def PopulationBuilder(self):

        thepopulation = []
        personindex = 0 
        for house in self.listOfResidentialBuildings:
            for floor in house.floors:
                for app in floor.appartments:
                    npeople = np.random.poisson(self.averagePopulationPerAppartment, 1)[0]
                    indexofpeople = []
                    for erson in range(0, npeople):
                        personId = 'person_' + str(personindex)
                        buildingworkplace = np.random.randint(0, self.nWorkPlaces, 1)[0]
                        floorworkplace = np.random.randint(0, self.listOfWorkBuildings[buildingworkplace].nFloors, 1)[0]
                        appartmentworkplace = np.random.randint(0, self.listOfWorkBuildings[buildingworkplace].floors[floorworkplace].nAppartments, 1)[0]
                        person = Person(personId, personindex, house.buildingId, floor.floorId, app.appartmentId, buildingworkplace, floorworkplace, appartmentworkplace) 
                        thepopulation.append(person)
                        indexofpeople.append(personindex) 
                        personindex = personindex + 1
                    app.assignPeople(indexofpeople)
        return thepopulation   
       

    ###################################################################################################
    ###################################################################################################
    def CountAppartments(self):

        a = 0
        for b in self.listOfResidentialBuildings:
            a = a + b.CountAppartments() 
        return a

    ###################################################################################################
    ###################################################################################################
    def Print(self):

        print('---------------------------------------------------')
        print('|               City Parameters                   |')
        print('---------------------------------------------------')
        print('City size: ' + str(self.size) + 'x' + str(self.size) + 'm2')
        print('Building size: ' + str(self.lBuilding) + 'x' + str(self.lBuilding) + 'm2')         
        print('Street width: ' + str(self.lStreet) + 'm')         
        print('Number of buildings: ' + str(self.nIter * self.nIter))
        print('Number of residential buildings: ' + str(self.nResidentialPlaces))
        print('Number of residential appartments: ' + str(self.nAppartmentResidentialPlaces))
        print('Number of work buildings: ' + str(self.nWorkPlaces))
        print('Number of leisure buildings: ' + str(self.nLeisurePlaces))
        print('Total population: ' + str(self.realPopulation))
        print('Average population per appartment: ' + str(self.averagePopulationPerAppartment))

        for b in self.listOfResidentialBuildings:
            b.Print()
        for b in self.listOfWorkBuildings:
            b.Print()
        for b in self.listOfLeisureBuildings:
            b.Print()
        for j in self.thePopulation:
            j.Print()




