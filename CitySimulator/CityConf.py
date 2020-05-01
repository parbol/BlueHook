###############################################################
#Python-based application for handling the info a city        #
###############################################################
import math

from CitySimulator.Building import Building
from CitySimulator.Floor import Floor
from CitySimulator.Appartment import Appartment


class CityConf:

    def __init__(self, confName):

        for i in open(confName).readlines():
            if i[0] == '#':
                continue
            if i == '\n':
                continue
            a = i.split()[0]
            b = i.split()[1]
            if a == 'size':
                self.size = float(b)
            if a == 'lBuilding':
                self.lBuilding = float(b)
            if a == 'lStreet':
                self.lStreet = float(b)
            if a == 'averagePopulationPerAppartment':
                self.averagePopulationPerAppartment = int(b)
            if a == 'fracRes':
                self.fracRes = float(b)
            if a == 'fracWor':
                self.fracWor = float(b)
            if a == 'fracLei':
                self.fracLei = float(b)
            if a == 'nFloorIndex':
                self.nFloorIndex= int(b)
            if a == 'nAppartmentIndex':
                self.nAppartmentIndex = int(b)
            if a == 'nHotPoints':
                self.nHotPoints = int(b)
            if a == 'lengthOfHotPoint':
                self.lengthOfHotPoint = float(b)
            if a == 'timescalehome':
                self.timescalehome = int(b)
            if a == 'timescalework':
                self.timescalework = int(b)
            if a == 'timescaleleisure':
                self.timescaleleisure = int(b)
            if a == 'timescaleleisuresite':
                self.timescaleleisuresite = int(b)
            if a == 'curationLambda':
                self.curationLambda = int(b) * 24 * 60
            if a == 'incubationLambda':
                self.incubationLambda = int(b) * 24 * 60
            if a == 'bluetoothRadius':
                self.bluetoothRadius = float(b)
            if a == 'infectionRadius':
                self.infectionRadius = float(b)
            if a == 'infectionProbability':
                self.infectionProbability = float(b)
            if a == 'timeToInfectLambda':
                self.timeToInfectLambda = int(b) * 24 * 60
            if a == 'noSymptomsProbability':
                self.noSymptomsProbability = float(b)
            if a == 'strategy':
                self.strategy = int(b)
            if a == 'numberOfTestsPerDay':
                self.numberOfTestsPerDay = int(b)
            if a == 'bluetoothTimeRange':
                self.bluetoothTimeRange = int(b) * 24 * 60
                                     
        self.instantInfectionProbability = 1.0 - math.pow(1 - self.infectionProbability, 1.0/30.0)
        self.lBlock = int(self.lBuilding + self.lStreet)
        self.nIter = int(self.size / self.lBlock)
        self.nBuildings = 0
        self.nResidentialBuildings = 0
        self.nWorkBuildings = 0
        self.nLeisureBuildings = 0
        self.nFloors = 0
        self.nResidentialFloors = 0
        self.nWorkFloors = 0
        self.nLeisureFloors = 0
        self.nResidentialAppartments = 0
        self.nWorkAppartments = 0
        self.nLeisureAppartments = 0
        self.realPopulation = 0

    ###################################################################################################
    ###################################################################################################
    def loadCityDetails(self, listOfBuildings, listOfResIndex, listOfWorkIndex, listOfLeisureIndex):

        self.nBuildings = len(listOfBuildings)
        self.nResidentialBuildings = len(listOfResIndex)
        self.nWorkBuildings = len(listOfWorkIndex)
        self.nLeisureBuildings = len(listOfLeisureIndex)
        self.nResidentialFloors = self.getFloors(listOfBuildings, listOfResIndex)
        self.nResidentialAppartments = self.getAppartments(listOfBuildings, listOfResIndex)
        self.nWorkFloors = self.getFloors(listOfBuildings, listOfWorkIndex)
        self.nWorkAppartments = self.getAppartments(listOfBuildings, listOfWorkIndex)
        self.nLeisureFloors = self.getFloors(listOfBuildings, listOfLeisureIndex)
        self.nLeisureAppartments = self.getAppartments(listOfBuildings, listOfLeisureIndex)
        self.nFloors = self.nResidentialFloors + self.nWorkFloors + self.nLeisureFloors
        self.nAppartments = self.nResidentialAppartments + self.nWorkAppartments + self.nLeisureAppartments

   ###################################################################################################
    ###################################################################################################
    def getFloors(self, thelist, theindex):

        totalfloors = 0
        for i in theindex:
            totalfloors = totalfloors + thelist[i].nFloors

        return totalfloors

    ###################################################################################################
    ###################################################################################################
    def getFloors(self, thelist, theindex):

        totalfloors = 0
        for i in theindex:
            totalfloors = totalfloors + thelist[i].nFloors
        return totalfloors

    ###################################################################################################
    ###################################################################################################
    def getAppartments(self, thelist, theindex):

        totalappartments = 0
        for i in theindex:
            for j in thelist[i].floors:
                totalappartments = totalappartments + j.nAppartments
        return totalappartments
    
    ###################################################################################################
    ###################################################################################################
    def loadPopulationDetails(self, pop):

        self.realPopulation = pop

    ###################################################################################################
    ###################################################################################################
    def Print(self):

        print('---------------------------------------------------')
        print('|               City Parameters                   |')
        print('---------------------------------------------------')
        print('City size: ' + str(self.size) + ' x ' + str(self.size) + 'm2')
        print('Building size: ' + str(self.lBuilding) + ' x ' + str(self.lBuilding) + 'm2')
        print('Street width: ' + str(self.lStreet) + 'm')
        print('Number of buildings: ' + str(self.nBuildings))
        print('Number of residential buildings: ' + str(self.nResidentialBuildings))
        print('Number of work buildings: ' + str(self.nWorkBuildings))
        print('Number of leisure buildings: ' + str(self.nLeisureBuildings))
        print('Number of floors: ' + str(self.nFloors))
        print('Number of residential floors: ' + str(self.nResidentialFloors))
        print('Number of work floors: ' + str(self.nWorkFloors))
        print('Number of leisure floors: ' + str(self.nLeisureFloors))
        print('Number of appartments: ' + str(self.nAppartments))
        print('Number of residential appartments: ' + str(self.nResidentialAppartments))
        print('Number of work appartments: ' + str(self.nWorkAppartments))
        print('Number of leisure appartments: ' + str(self.nLeisureAppartments))
        print('Total population: ' + str(self.realPopulation))
        print('Average population per appartment: ' + str(self.averagePopulationPerAppartment))



 

 


  

