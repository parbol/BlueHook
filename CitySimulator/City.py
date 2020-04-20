###############################################################
#Python-based application for handling a city                 #
###############################################################
import numpy as np

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
        
    def BuildingBuilder(self):

        buildingsResidential = []
        buildingsWork = []
        buildingsLeisure = []
        nAppartmentResidential = 0
        nAppartmentWork = 0
        nAppartmentLeisure = 0

        for i in range(0, self.nIter):
            for j in range(0, self.nIter):
                #Building Id
                theid = 'building_' + str(i) + '_' + str(j)
                #Type of building  
                dice = np.random.uniform(0, 1, 1)
                if dice < self.fracRes:
                    thefloors = 1 + np.random.poisson(self.nFloorIndex, 1)[0]
                    theappartments = 1 + np.random.poisson(self.nAppartmentIndex, 1)[0]
                    nAppartmentResidential = nAppartmentResidential + (theappartments * thefloors)
                    thebuilding = Building(theid, self.lBuilding, i * self.lBlock + self.lStreet + self.lBuilding/2.0, j * self.lBlock + self.lStreet + self.lBuilding/2.0, 0, thefloors, theappartments)
                    buildingsResidential.append(thebuilding)
                elif dice >= self.fracRes and dice < (self.fracWor + self.fracRes):
                    thefloors = 1 + np.random.poisson(self.nFloorIndex, 1)[0]
                    theappartments = 1 + np.random.poisson(self.nAppartmentIndex, 1)[0]
                    nAppartmentWork = nAppartmentWork + theappartments * thefloors
                    thebuilding = Building(theid, self.lBuilding, i * self.lBlock + self.lStreet + self.lBuilding/2.0, j * self.lBlock + self.lStreet + self.lBuilding/2.0, 1, thefloors, theappartments)
                    buildingsWork.append(thebuilding)
                else:
                    thefloors = 1 
                    theappartments = 1 + np.random.poisson(self.nAppartmentIndex, 1)[0]
                    nAppartmentLeisure = nAppartmentLeisure + theappartments * thefloors
                    thebuilding = Building(theid, self.lBuilding, i * self.lBlock + self.lStreet + self.lBuilding/2.0, j * self.lBlock + self.lStreet + self.lBuilding/2.0, 2, thefloors, theappartments)
                    buildingsLeisure.append(thebuilding)
        return [[buildingsResidential, nAppartmentResidential], [buildingsWork, nAppartmentWork], [buildingsLeisure, nAppartmentLeisure]]
   
   
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
       

    def CountAppartments(self):

        a = 0
        for b in self.listOfResidentialBuildings:
            a = a + b.CountAppartments() 
        return a

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




