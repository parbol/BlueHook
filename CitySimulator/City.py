###############################################################
#Python-based application for handling a city                 #
###############################################################
from CitySimulator.Building import Building
from CitySimulator.Person import Person
from CitySimulator.CityConf import CityConf

import numpy as np
import math


###############################################################
###############################################################
class City:

    def __init__(self, confName):
 
        #Internal parameters of the city
        self.conf = CityConf(confName) 

        #Creating the places of the city
        listOfBuildings = self.BuildingBuilder()
        #This is the main list of buildings  
        self.buildings = listOfBuildings[0]
        #These are the indexes of the residential, working and leisure buildings
        self.residentialBuildingIndexes = listOfBuildings[1]
        self.workBuildingIndexes = listOfBuildings[2]
        self.leisureBuildingIndexes = listOfBuildings[3]
        
        #Update the information of the city with its current implementation
        self.conf.loadCityDetails(self.buildings, self.residentialBuildingIndexes, self.workBuildingIndexes, self.leisureBuildingIndexes)
        
        #Creating the population
        self.thePopulation = self.PopulationBuilder()
        self.conf.loadPopulationDetails(len(self.thePopulation))


    ###################################################################################################
    ###################################################################################################
    def BuildingBuilder(self):

        #Use this variable as building global index
        building = 0
        buildings = []

        residentialBuildingIndexes = []
        workBuildingIndexes = []
        leisureBuildingIndexes = []
        
        for i in range(0, self.conf.nIter):
            for j in range(0, self.conf.nIter):
                #Type of building  
                dice = np.random.uniform(0, 1, 1)
                if dice < self.conf.fracRes:
                    thebuilding = Building(building, self.conf, i, j, 0)
                    buildings.append(thebuilding)
                    residentialBuildingIndexes.append(building)
                elif dice >= self.conf.fracRes and dice < (self.conf.fracWor + self.conf.fracRes):
                    thebuilding = Building(building, self.conf, i, j, 1)
                    buildings.append(thebuilding)
                    workBuildingIndexes.append(building)
                else:
                    thebuilding = Building(building, self.conf, i, j, 2)
                    buildings.append(thebuilding)
                    leisureBuildingIndexes.append(building)
                building = building + 1
     
        return [buildings, residentialBuildingIndexes, workBuildingIndexes, leisureBuildingIndexes]
 
   
    ###################################################################################################
    ###################################################################################################
    def PopulationBuilder(self):

        thepopulation = []
        personindex = 0 
        for index in self.residentialBuildingIndexes:
            house = self.buildings[index] 
            for floor in house.floors:
                for app in floor.appartments:
                    npeople = np.random.poisson(self.conf.averagePopulationPerAppartment, 1)[0]
                    indexofpeople = []
                    for person in range(0, npeople):
                        personId = 'person_' + str(personindex)
                        buildingworkplace = self.workBuildingIndexes[np.random.randint(0, self.conf.nWorkBuildings, 1)[0]]
                        floorworkplace = np.random.randint(0, self.buildings[buildingworkplace].nFloors, 1)[0]
                        appartmentworkplace = np.random.randint(0, self.buildings[buildingworkplace].floors[floorworkplace].nAppartments, 1)[0]
                        person = Person(personId, personindex, house.building, floor.floor, app.appartment, buildingworkplace, floorworkplace, appartmentworkplace) 
                        thepopulation.append(person)
                        indexofpeople.append(personindex) 
                        personindex = personindex + 1
                    app.assignPeople(indexofpeople)
        return thepopulation   
       
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
        #self.match(time)

    ###################################################################################################
    ###################################################################################################
    #def match(self, time):
    
    #    for building in self.buildings:
    #        for floor in building.floors:
    #            for app in floor.appartments:
    #                for p in app.persons:

                    
    

    ###################################################################################################
    ###################################################################################################
    def goHome(self, person):
        
        self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].removePerson(person.theId)  
        person.lastposition = 0
        person.activeBuilding = person.residentialBuilding
        person.activeFloor = person.residentialFloor
        person.activeAppartment = person.residentialAppartment
        self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].addPerson(person.theId)  
        [person.x, person.y] = self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].GetRandomPosition()
        person.howlongcounter = 0
        person.howlong = np.random.poisson(self.conf.timescalehome, 1)[0]

    ###################################################################################################
    ###################################################################################################
    def runHome(self, person):

        person.howlongcounter = person.howlongcounter + 1
        if person.howlongcounter >= person.howlong:
            [person.x, person.y] = self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].GetRandomPosition()
            person.howlongcounter = 0
            person.howlong = np.random.poisson(self.conf.timescalehome, 1)[0]

    ###################################################################################################
    ###################################################################################################
    def goWork(self, person):

        self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].removePerson(person.theId)  
        person.lastposition = 1
        person.activeBuilding = person.workplaceBuilding 
        person.activeFloor = person.workplaceFloor
        person.activeAppartment = person.workplaceAppartment
        self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].addPerson(person.theId)  
        [person.x, person.y] = self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].GetRandomPosition()
        person.howlongcounter = 0
        person.howlong = np.random.poisson(self.conf.timescalework, 1)[0]

    ###################################################################################################
    ###################################################################################################
    def runWork(self, person):

        person.howlongcounter = person.howlongcounter + 1
        if person.howlongcounter >= person.howlong:
            [person.x, person.y] = self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].GetRandomPosition()
            self.howlongcounter = 0
            self.howlong = np.random.poisson(self.conf.timescalework, 1)[0]

    ###################################################################################################
    ###################################################################################################
    def goLeisure(self, person):

        self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].removePerson(person.theId)  
        person.lastposition = 2
        person.leisurehowlong = np.random.poisson(self.conf.timescaleleisuresite, 1)[0]
        person.leisurehowlongcounter = 0
        person.activeBuilding = self.buildings[self.leisureBuildingIndexes[np.random.randint(0, self.conf.nLeisureBuildings, 1)[0]]].building
        person.activeFloor = 0
        person.activeAppartment = np.random.randint(0, self.buildings[person.activeBuilding].floors[0].nAppartments, 1)[0]
        self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].addPerson(person.theId)
        [person.x, person.y] = self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].GetRandomPosition()
        person.howlongcounter = 0
        person.howlong = np.random.poisson(self.conf.timescaleleisure, 1)[0]


    ###################################################################################################
    ###################################################################################################
    def runLeisure(self, person):
        
        person.howlongcounter = person.howlongcounter + 1
        person.leisurehowlongcounter = person.leisurehowlongcounter + 1
        if person.leisurehowlongcounter >= person.leisurehowlong:
            person.leisurehowlong = np.random.poisson(self.conf.timescaleleisuresite, 1)[0]
            person.leisurehowlongcounter = 0 
            self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].removePerson(person.theId)  
            person.activeBuilding = self.buildings[self.leisureBuildingIndexes[np.random.randint(0, self.conf.nLeisureBuildings, 1)[0]]].building
            person.activeFloor = 0
            person.activeAppartment = np.random.randint(0, self.buildings[person.activeBuilding].floors[0].nAppartments, 1)[0]
            self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].addPerson(person.theId)
            [person.x, person.y] = self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].GetRandomPosition()
            person.howlongcounter = 0
            person.howlong = np.random.poisson(self.conf.timescaleleisure, 1)[0]
 
        if person.howlongcounter >= person.howlong:
            [person.x, person.y] = self.buildings[person.activeBuilding].floors[0].appartments[person.activeAppartment].GetRandomPosition()
            person.howlongcounter = 0
            person.howlong = np.random.poisson(self.conf.timescaleleisure, 1)[0]
        
    ###################################################################################################
    ###################################################################################################
    def Print(self, level):

        self.conf.Print()

        if level > 1:
            for b in self.buildings:
                b.Print()
            for j in self.thePopulation:
                j.Print()

    ###################################################################################################
    ###################################################################################################
    def getHour(self, time):

        days = math.floor(time / (24.0*60.0))
        newtime = time - days * 24
        hour = math.floor(newtime / 60)
        return hour


