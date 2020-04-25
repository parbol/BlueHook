###############################################################
#Python-based application for handling a city                 #
###############################################################
from CitySimulator.Building import Building
from CitySimulator.Person import Person
from CitySimulator.CityConf import CityConf

from JanusAPI.JanusServer import JanusServer


import numpy as np
import math
import itertools

###############################################################
###############################################################
class City:

    def __init__(self, confName, serverlocation, filename, seed):
 
        np.random.seed(seed)

        self.janus = JanusServer(serverlocation)
        self.filename = filename

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
        #Self time
        self.time = 0
        #Update the information of the city with its current implementation
        self.conf.loadCityDetails(self.buildings, self.residentialBuildingIndexes, self.workBuildingIndexes, self.leisureBuildingIndexes)

        self.nHealthy = 0
        self.nInfected = 0
        self.nCured = 0
        
        self.days = []
        self.healthy = []
        self.infected = []
        self.cured = []
        
        #Creating the population
        self.thePopulation = self.PopulationBuilder()
        self.conf.loadPopulationDetails(len(self.thePopulation))
        self.update()


    ###################################################################################################
    ###################################################################################################
    def BuildingBuilder(self):

        #Use this variable as building global index
        building = 0
        buildings = []

        residentialBuildingIndexes = []
        workBuildingIndexes = []
        leisureBuildingIndexes = []
        tot = self.conf.nIter * self.conf.nIter

        for i in range(0, self.conf.nIter):
            for j in range(0, self.conf.nIter):
                dice = building / tot
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
                        person = Person(personId, personindex, house.building, floor.floor, app.appartment, buildingworkplace, floorworkplace, appartmentworkplace, self.conf) 
                        thepopulation.append(person)
                        indexofpeople.append(personindex) 
                        personindex = personindex + 1
                    app.assignPeople(indexofpeople)
        thepopulation[0].infect(self.time)
        return thepopulation   

       
    ###################################################################################################
    ###################################################################################################
    def runDays(self, days):
        
        self.Print(1) 
        for i in range(0, days):
            self.checkStats(i)
            self.runDay(i)
        self.Save()

    ###################################################################################################
    ###################################################################################################
    def runDay(self, day):

        for j in range(0, 24*60):
            self.runMinute()
            self.time = self.time + 1
    
    ###################################################################################################
    ###################################################################################################
    def runMinute(self):

        theTime = self.time % 1440 
        for person in self.thePopulation:
            if person.quarantine == 1:
                if person.lastposition != 0:
                    self.goHome(person)
                else:
                    self.runHome(person)
            else:
                if theTime >= person.timeToGoHome:
                    if person.lastposition == 2:
                        self.goHome(person)
                    else:
                        self.runHome(person)
                elif theTime < person.timeToGoToWork:
                    if person.lastposition == 2:
                        self.goHome(person)
                    else:
                        self.runHome(person)
                elif theTime >= person.timeToGoToWork and theTime < person.timeToLeaveWork:
                    if person.lastposition == 0:
                        self.goWork(person)
                    else:
                        self.runWork(person)
                elif theTime >= person.timeToLeaveWork and theTime < person.timeToGoHome:
                    if person.lastposition == 1:
                        self.goLeisure(person)
                    else:
                        self.runLeisure(person)
            if theTime == person.bluetoothUpdate:
                person.updateBluetooth(self.janus)
        self.match()
        #print('Time: ' + str(self.time))
        #self.tracking(0)

    ###################################################################################################
    ###################################################################################################
    def match(self):
   
        matchInfection = set()
        matchBluetooth = set()
 
        #Find the pairs
        for building in self.buildings:
            for floor in building.floors:
                for app in floor.appartments:
                    #Tracking infections
                    if len(app.persons) == 0:
                        continue
                    for i in itertools.product(app.persons, app.persons):
                        if i[0] <= i[1]:
                            continue
                        if not (self.thePopulation[i[0]].canInfect == 1 or self.thePopulation[i[1]].canInfect == 1):
                            continue 
                        if self.thePopulation[i[0]].health == 1 and self.thePopulation[i[1]].health == 1:
                            continue
                        if self.thePopulation[i[0]].health == 2 or self.thePopulation[i[1]].health == 2:
                            continue
                        x1 = self.thePopulation[i[0]].x
                        x2 = self.thePopulation[i[1]].x
                        y1 = self.thePopulation[i[0]].y
                        y2 = self.thePopulation[i[1]].y
                        if math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)) > self.conf.infectionRadius:
                            continue 
                        matchInfection.add(i) 
                    #Tracking bluetooth contacts
                    listOfPersons = app.persons
                    if len(listOfPersons) == 0:
                        continue
                    if app.floor == 0 and building.nFloors > 1:
                        listOfPersons = listOfPersons + building.floors[1].appartments[app.appartment].persons
                    elif app.floor == building.nFloors - 1 and building.nFloors > 1:
                        listOfPersons = listOfPersons + building.floors[building.nFloors - 1].appartments[app.appartment].persons
                    for i in itertools.product(listOfPersons, listOfPersons):
                        if i[0] <= i[1]:
                            continue
                        x1 = self.thePopulation[i[0]].x
                        x2 = self.thePopulation[i[1]].x
                        y1 = self.thePopulation[i[0]].y
                        y2 = self.thePopulation[i[1]].y
                        z1 = self.thePopulation[i[0]].z
                        z2 = self.thePopulation[i[1]].z
                        if math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) + (z1-z2)*(z1-z2)) > self.conf.bluetoothRadius:
                            continue 
                        matchBluetooth.add(i) 
 
        #Going for infections
        for i in matchInfection:
            self.infect(i[0], i[1])
                        
        #Going for bluetooth contact
        for i in matchBluetooth:
            self.bluetooth(i[0], i[1])
        #Update the clinical state of everyone
        self.update()
                        
    ###################################################################################################
    ###################################################################################################
    def infect(self, person1, person2):
        #print('Infection between ' + str(person1) + ' ' + str(person2))
        dice = np.random.uniform(0, 1, 1)[0]
        if dice < self.conf.instantInfectionProbability:
            if self.thePopulation[person1].health == 1:
                self.thePopulation[person2].infect(self.time)
            else:
                self.thePopulation[person1].infect(self.time)

    ###################################################################################################
    ###################################################################################################
    def bluetooth(self, person1, person2):
    
        self.thePopulation[person1].bluetoothMatch(person2, self.thePopulation[person1].x, self.thePopulation[person1].y, self.time)
        self.thePopulation[person2].bluetoothMatch(person1, self.thePopulation[person2].x, self.thePopulation[person2].y, self.time)

    ###################################################################################################
    ###################################################################################################
    def clearBluetooth(self):

        for i in self.thePopulation:
            i.bluetoothmatches.clear()

    ###################################################################################################
    ###################################################################################################
    def update(self):

        self.nHealthy = 0
        self.nInfected = 0
        self.nCured = 0
        #For each person
        for i in self.thePopulation:
            #If healthy -> update
            if i.health == 0:
                i.health = i.newHealth
            #If infected
            if i.health == 1:
                #If cured
                if self.time > i.timeOfCuration:
                    i.health = 2
                    i.symptoms = 0
                    i.quarantine = 0 
                    i.canInfect = 0
                #If presenting symptoms
                elif self.time > i.timeOfIncubation:
                    if i.hasSymptoms:
                        i.symptoms = 1
                        i.quarantine = 1
                #If passed infection time
                elif self.time > i.timeToInfect:
                    i.canInfect = 1
            if i.health == 0:
                self.nHealthy = self.nHealthy + 1
            elif i.health == 1:
                self.nInfected = self.nInfected + 1
            else:
                self.nCured = self.nCured + 1


    ###################################################################################################
    ###################################################################################################
    def goHome(self, person):

        person.setHours()
        self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].removePerson(person.person)  
        person.lastposition = 0
        person.activeBuilding = person.residentialBuilding
        person.activeFloor = person.residentialFloor
        person.activeAppartment = person.residentialAppartment
        self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].addPerson(person.person)  
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

        self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].removePerson(person.person)  
        person.lastposition = 1
        person.activeBuilding = person.workplaceBuilding 
        person.activeFloor = person.workplaceFloor
        person.activeAppartment = person.workplaceAppartment
        self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].addPerson(person.person)  
        [person.x, person.y] = self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].GetRandomPosition()
        person.howlongcounter = 0
        person.howlong = np.random.poisson(self.conf.timescalework, 1)[0]

    ###################################################################################################
    ###################################################################################################
    def runWork(self, person):

        person.howlongcounter = person.howlongcounter + 1
        if person.howlongcounter >= person.howlong:
            [person.x, person.y] = self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].GetRandomPosition()
            person.howlongcounter = 0
            person.howlong = np.random.poisson(self.conf.timescalework, 1)[0]

    ###################################################################################################
    ###################################################################################################
    def goLeisure(self, person):

        self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].removePerson(person.person)  
        person.lastposition = 2
        person.leisurehowlong = np.random.poisson(self.conf.timescaleleisuresite, 1)[0]
        person.leisurehowlongcounter = 0
        person.activeBuilding = self.buildings[self.leisureBuildingIndexes[np.random.randint(0, self.conf.nLeisureBuildings, 1)[0]]].building
        person.activeFloor = 0
        person.activeAppartment = np.random.randint(0, self.buildings[person.activeBuilding].floors[0].nAppartments, 1)[0]
        self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].addPerson(person.person)
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
            self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].removePerson(person.person)  
            person.activeBuilding = self.buildings[self.leisureBuildingIndexes[np.random.randint(0, self.conf.nLeisureBuildings, 1)[0]]].building
            person.activeFloor = 0
            person.activeAppartment = np.random.randint(0, self.buildings[person.activeBuilding].floors[0].nAppartments, 1)[0]
            self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].addPerson(person.person)
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
    def checkStats(self, day):

        print('----------------Stats--------------------')
        print('Day: ', str(day))
        print('Number of healthy people: ' + str(self.nHealthy) + ', number of infected people: ' + str(self.nInfected) + ', number of cured people: ' + str(self.nCured))  
        self.days.append(day)
        self.healthy.append(self.nHealthy)
        self.infected.append(self.nInfected)
        self.cured.append(self.nCured)

    ####################################################################################################
    ###################################################################################################
    def Save(self):

        thelist = [self.days, self.healthy, self.infected, self.cured]
        nparr = np.asarray(thelist)
        np.savetxt(self.filename, nparr, delimiter=',')

    ###################################################################################################
    ###################################################################################################
    def tracking(self, n):

        self.thePopulation[n].Print()
        #print('The active building') 
        #self.buildings[self.thePopulation[n].activeBuilding].floors[self.thePopulation[n].activeFloor].appartments[self.thePopulation[n].activeAppartment].Print()
        #print('The residential building') 
        #self.buildings[self.thePopulation[n].residentialBuilding].floors[self.thePopulation[n].residentialFloor].appartments[self.thePopulation[n].residentialAppartment].Print()
        #print('The working building') 
        #self.buildings[self.thePopulation[n].workplaceBuilding].floors[self.thePopulation[n].workplaceFloor].appartments[self.thePopulation[n].workplaceAppartment].Print()

    ###################################################################################################
    ###################################################################################################
    def getHour(self):

        days = math.floor(self.time / (24.0*60.0))
        newtime = self.time - days * 24
        hour = math.floor(newtime / 60)
        return hour


