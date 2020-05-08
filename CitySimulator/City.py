###############################################################
#Python-based application for handling a city                 #
###############################################################
from CitySimulator.Building import Building
from CitySimulator.Person import Person
from CitySimulator.CityConf import CityConf

from JanusAPI.JanusServer import JanusServer

import math
import itertools
import random
import numpy as np


###############################################################
###############################################################
class City:

    def __init__(self, confName, serverlocation, filename, seed, seedCity, mode, paint):
 
        random.seed(seedCity)

        self.janus = JanusServer(serverlocation, mode)
        self.filename = filename
        self.paint = paint
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
        self.nQuarantine=0

        self.days = []
        self.healthy = []
        self.infected = []
        self.cured = []
        self.tested=[]
        self.nquarantine=[]
        
     	#Creating the population
        self.thePopulation = self.PopulationBuilder()

        #Turning on the bluetooth according to the engagement
        switchOnBluetooth=random.sample(range(len(self.thePopulation)), k=int(self.conf.appEngagement*len(self.thePopulation)/100))
        for citizen in self.thePopulation:
             if citizen.person in switchOnBluetooth:
                 citizen.bluetoothOn=1

        self.conf.loadPopulationDetails(len(self.thePopulation))

        if self.paint != -1:
            self.fileToSave = open('geometry.txt', 'w')
            self.fileToSave.write('citysize ' + str(self.conf.size) + '\n')
            self.fileToSave.write('lbuilding ' + str(self.conf.lBuilding) + '\n')
            self.fileToSave.write('lstreet ' + str(self.conf.lStreet) + '\n')
            self.fileToSave.write('population ' + str(self.conf.realPopulation) + '\n')
            for i in self.buildings:
                self.fileToSave.write(str(i.floors[0].nAppartmentsPerSide) + ' ' + str(i.floors[0].lAppartment) + '\n')
        self.update()
        
        random.seed(seed)
        for i in self.thePopulation:
            self.goHome(i)
        self.contactsInfection = []
        self.contactsBluetooth = []
        self.createContactsInfection()
        self.createContactsBluetooth()

   ###################################################################################################
    ###################################################################################################
    def createContactsInfection(self):

        for i in range(0, self.conf.realPopulation):
            self.contactsInfection.append([])

    ###################################################################################################
    ###################################################################################################
    def createContactsBluetooth(self):

        for i in range(0, self.conf.realPopulation):
            self.contactsBluetooth.append([])

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
                dice = random.random()
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
                    npeople = int(round(random.gammavariate(self.conf.averagePopulationPerAppartment, 1)))
                    indexofpeople = []
                    for individual in range(0, npeople):
                        personId = 'person_' + str(personindex)
                        buildingworkplace = self.workBuildingIndexes[random.randint(0, self.conf.nWorkBuildings-1)]
                        floorworkplace = random.randint(0, self.buildings[buildingworkplace].nFloors-1)
                        appartmentworkplace = random.randint(0, self.buildings[buildingworkplace].floors[floorworkplace].nAppartments-1)
                        person = Person(personId, personindex, house.building, floor.floor, app.appartment, buildingworkplace, floorworkplace, appartmentworkplace, self.conf) 
                        thepopulation.append(person)
                        indexofpeople.append(personindex)
                        personindex = personindex + 1
                    app.assignPeople(indexofpeople)
                    app.inhabitants=[x for x in indexofpeople]
        thepopulation[0].infect(self.time)
        return thepopulation   

       
    ###################################################################################################
    ###################################################################################################
    def runDays(self, days):
        self.Print(1) 
        for i in range(0, days):
            self.runDay(i)
        self.Save()
        if self.paint != -1:
            self.fileToSave.close()
    ###################################################################################################
    ###################################################################################################
    def runDay(self, day):
        self.checkStats(day)
        if self.nQuarantine > 0:
            self.runTests(day)
        for j in range(0, 24*60):
            self.runMinute()
            self.time = self.time + 1
            if self.paint != -1:
                if j % self.paint == 0:
                    self.storeGeometricInfo()
	
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
                if person.lastposition == 0:
                    if theTime < person.timeToGoToWork or theTime >= person.oldTimeToGoHome:
                        self.runHome(person)
                    else:
                        self.goWork(person)  
                elif person.lastposition == 1:
                    if theTime < person.timeToLeaveWork:
                        self.runWork(person)
                    else:
                        self.goLeisure(person)
                elif person.lastposition == 2:
                    if theTime < person.timeToGoHome:
                        self.runLeisure(person)
                    else:
                        self.goHome(person)
            if theTime == person.bluetoothUpdate:
                person.updateBluetooth(self.janus)
        self.match()
        #Update the clinical state of everyone
        self.update()
        #print('Time: ' + str(self.time) + ' Day: ' + str(int(self.time/(24*60))) + ' Hour: ' + str(self.getHour()))
        #self.tracking(34)

   ###################################################################################################
   ###################################################################################################

    def suspiciousFamilies(self):
        totalSuspiciousFamilies=[]
        #For each person
        for i in self.thePopulation:
            suspiciousFamily=[]
            if i.quarantine==1:
                #print('Person ' + str(i.person) + ' in quarantine')
                #ibuild=i.residentialBuilding
                #ifloor=i.residentialFloor
                #iappart=i.residentialAppartment
                #print('With this person live: ', self.buildings[ibuild].floors[ifloor].appartments[iappart].inhabitants)
                #List with people living in the same house
                suspiciousFamily=[x for x in self.buildings[i.residentialBuilding].floors[i.residentialFloor].appartments[i.residentialAppartment].inhabitants if x!=i.person]
            totalSuspiciousFamilies+=suspiciousFamily
        return(set(totalSuspiciousFamilies))

   ###################################################################################################
   ###################################################################################################


    def suspiciousBluetoothMatches(self):
        totalSuspiciousMatches=[]
        for i in self.thePopulation:
            suspiciousMatches=[]
            if conf.self.strategy == 3 or conf.self.strategy==4:
                if i.quarantine==1:
                #List with people bluetooth matched
                #print('Person ' + str(i.person) + ' in quarantine')
                #print('Contacts of person are: ')
                #print(i.bluetoothOldMatches)
                    for j in i.bluetoothOldMatches:
                        if (self.time - j[3]) < self.conf.bluetoothTimeRange and j[4] >= self.conf.minBluetoothTime:
                            suspiciousMatches.append(j[0])
                totalSuspiciousMatches+=suspiciousMatches

            if conf.self.strategy == 5:
                if i.symptoms==1 or i.positiveTested==1:
                #List with people bluetooth matched
                #print('Person ' + str(i.person) + ' in quarantine')
                #print('Contacts of person are: ')
                #print(i.bluetoothOldMatches)
                    for j in i.bluetoothOldMatches:
                        if (self.time - j[3]) < self.conf.bluetoothTimeRange and j[4] >= self.conf.minBluetoothTime:
                            suspiciousMatches.append(j[0])
                totalSuspiciousMatches+=suspiciousMatches

        return(set(totalSuspiciousMatches))

   ###################################################################################################
   ###################################################################################################


    def runTests(self,day):
       
        strategy=self.conf.strategy
        #No testing - strategy 0
        if (strategy==0):
            return 

        #Random testing - strategy 1
        if (strategy==1):
            notYetTested=[x for x in range(self.conf.realPopulation) if x not in self.tested and self.thePopulation[x].quarantine!=1 and self.thePopulation[x].health !=2]
             
        #Testing families - strategy 2
        if (strategy==2):
            notYetTested=[x for x in self.suspiciousFamilies() if x not in self.tested and self.thePopulation[x].quarantine!=1 and self.thePopulation[x].health !=2]

        #Testing bluetooth matches - strategy 3 and putting in quarantine all the bluetooth matches - strategy 4
        if (strategy ==3 or strategy ==4):
            notYetTested=[x for x in self.suspiciousBluetoothMatches() if x not in self.tested and self.thePopulation[x].quarantine!=1 and self.thePopulation[x].health!=2]
            #print('Testing: ')
            #print(notYetTested)


        #Testing bluetooth matches and sending the no tested to quarantine - strategy 5
        if (strategy == 5):
            notYetTested=[x for x in self.suspiciousBluetoothMatches() if x not in self.tested and self.thePopulation[x].symptoms==0 and self.thePopulation[x].health!=2]
            #print('Testing: ')
            #print(notYetTested)

        #Check if the total numbers of test is bigger than the population to be tested
        if strategy < 4:
            if len(notYetTested) >= self.conf.numberOfTestsPerDay:
                dailyTested=random.sample(notYetTested, k=self.conf.numberOfTestsPerDay)
            else:
                dailyTested=notYetTested
           
            for i in dailyTested:
                #print('Testing: ', i)
                #resb = self.thePopulation[i].residentialBuilding
                #resf = self.thePopulation[i].residentialFloor
                #resa = self.thePopulation[i].residentialAppartment
                citizen=self.thePopulation[i]
                if citizen.health == 1:
                    citizen.quarantine = 1
                    citizen.positiveTested=1
                    self.tested.append(i)
 
        elif strategy == 4:
            dailyTested=notYetTested
            for i in dailyTested:
                citizen=self.thePopulation[i]
                citizen.quarantine = 1

        elif strategy == 5:

            if len(notYetTested) >= self.conf.numberOfTestsPerDay:
                dailyTested=random.sample(notYetTested, k=self.conf.numberOfTestsPerDay)
            else:
                dailyTested=notYetTested

            for i in dailyTested:
                #print('Testing: ', i)
                #resb = self.thePopulation[i].residentialBuilding
                #resf = self.thePopulation[i].residentialFloor
                #resa = self.thePopulation[i].residentialAppartment
                citizen=self.thePopulation[i]
                if citizen.health == 1:
                    citizen.quarantine = 1
                    citizen.positiveTested=1
                    self.tested.append(i)
                elif citizen.health == 0:
                    if citizen.quarantine ==1:
                        citizen.quarantine ==0
                        #print("Dear people from Smallport, we just freed one of your citizens from quarantine directly into a pandemic world!")
                        #print("God protect the poor soul!") 


            #print(dailyTested)
            dailyQuarantined=[x for x in notYetTested if x not in dailyTested]
            for i in dailyQuarantined:
                self.thePopulation[i].quarantine=1

    ###################################################################################################
    ###################################################################################################
    def match2(self):

        #Tracking bluetooth contacts

        for person in self.thePopulation:
            if person.newposition == 1:
                if self.conf.strategy > 2:
                    thecontactsbluetooth = self.contactsBluetooth[person.person]
                    print('Person: ' + str(person.person), thecontactsbluetooth)
                    for i in thecontactsbluetooth:
                        print(self.contactsBluetooth[i])
                        self.contactsBluetooth[i].remove(person.person)
                thecontactsinfection = self.contactsInfection[person.person]
                for i in thecontactsinfection:
                    self.contactsInfection[i].remove(person.person)
                self.updateMatches(person.person)
                person.newposition = 0

        for i, cont in enumerate(self.contactsInfection):
            if self.thePopulation[i].health != 0:
                continue
            else:
                for j in cont:
                    if self.thePopulation[j].canInfect == 1:
                        self.infect2(i, j)
        if self.conf.strategy > 2: 
            for i, cont in enumerate(self.contactsBluetooth):
                for j in cont:
                    if i < j:
                        self.bluetooth(i, j)

    ###################################################################################################
    ###################################################################################################
    def updateMatches(self, i):

        building = self.buildings[self.thePopulation[i].activeBuilding]
        floor = building.floors[self.thePopulation[i].activeFloor]
        app = floor.appartments[self.thePopulation[i].activeAppartment]
        
        self.contactsInfection[i].clear()

        peopleInTheRoom = app.persons
        for j in peopleInTheRoom:
            if j == i:
                continue
            x1 = self.thePopulation[i].x
            x2 = self.thePopulation[j].x
            y1 = self.thePopulation[i].y
            y2 = self.thePopulation[j].y
            if math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)) > self.conf.infectionRadius:
                continue
            if j not in self.contactsInfection[i]:
                self.contactsInfection[i].append(j)
                self.contactsInfection[j].append(i)
        
        if self.conf.strategy > 2:
            #Catching the upper and lower appartmens (if any)
            if building.nFloors > 1:
                if app.floor == 0:
                    peopleInTheRoom = peopleInTheRoom + building.floors[1].appartments[app.appartment].persons
                elif app.floor == building.nFloors - 1:
                    peopleInTheRoom = peopleInTheRoom + building.floors[building.nFloors - 2].appartments[app.appartment].persons
                else:
                    peopleInTheRoom = peopleInTheRoom + building.floors[app.floor - 1].appartments[app.appartment].persons + building.floors[app.floor + 1].appartments[app.appartment].persons
                #Catching the sides (if any)
            if floor.nAppartments > 1:
               for s in [-1, 0, 1]:
                   for t in [-1, 0, 1]:
                       if abs(s*t) == 1:
                           continue
                       if s == 0 and t == 0:
                           continue
                       k = floor.existsApp(app.i + s, app.j + t)
                       if k >= 0:
                           peopleInTheRoom = peopleInTheRoom + building.floors[app.floor].appartments[k].persons 
                           
            for j in peopleInTheRoom:
                if j == i:
                    continue
                x1 = self.thePopulation[i].x
                x2 = self.thePopulation[j].x
                y1 = self.thePopulation[i].y
                y2 = self.thePopulation[j].y
                z1 = self.thePopulation[i].z
                z2 = self.thePopulation[j].z
                if math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) + (z1-z2)*(z1-z2)) > self.conf.bluetoothRadius:
                   continue 
            if j not in self.contactsBluetooth[i]:
                self.contactsBluetooth[i].append(j)
                self.contactsBluetooth[j].append(i)

    ###################################################################################################
    ###################################################################################################
    def match(self):
   
        matchInfection = set()
        matchBluetooth = set()
        matchBluetooth2 = set()
 
        #Find the pairs
        for building in self.buildings:
            for floor in building.floors:
                for app in floor.appartments:
                    #Tracking infections
                    if len(app.persons) == 0:
                        continue
                    healthypeople = [x for x in app.persons if self.thePopulation[x].health == 0]
                    caninfectpeople = [x for x in app.persons if self.thePopulation[x].canInfect == 1 and not self.thePopulation[x].quarantine == 1]
                    for i in itertools.product(healthypeople, caninfectpeople):
                        #if i[0] <= i[1]:
                        #    continue
                        #x1 = self.thePopulation[i[0]].x
                        #x2 = self.thePopulation[i[1]].x
                        #y1 = self.thePopulation[i[0]].y
                        #y2 = self.thePopulation[i[1]].y
                        #if math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)) < self.conf.infectionRadius:
                        #    self.fileToSave.write('Contact ' + str(i[0]) + ' ' +  str(i[1]) + ' ' + str(self.time) + '\n') 
                        #if not (self.thePopulation[i[0]].canInfect == 1 or self.thePopulation[i[1]].canInfect == 1):
                        #    continue 
                        #if self.thePopulation[i[0]].health == 1 and self.thePopulation[i[1]].health == 1:
                        #    continue
                        #if self.thePopulation[i[0]].health == 2 or self.thePopulation[i[1]].health == 2:
                        #    continue
                        #if self.thePopulation[i[0]].quarantine == 1 or self.thePopulation[i[1]].quarantine == 1:
                        #    continue
                        x1 = self.thePopulation[i[0]].x
                        x2 = self.thePopulation[i[1]].x
                        y1 = self.thePopulation[i[0]].y
                        y2 = self.thePopulation[i[1]].y
                        if math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)) > self.conf.infectionRadius:
                            continue 
                        matchInfection.add(i) 
                    #Tracking bluetooth contacts
                    if self.conf.strategy > 2:
                        listOfPersonsWithBluetooth = [x for x in app.persons if (self.thePopulation[x].quarantine == 0 and self.thePopulation[x].bluetoothOn != 0)]
                        for i in itertools.product(listOfPersonsWithBluetooth, listOfPersonsWithBluetooth):
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
                            #This list is for bluetooth contacts to be inserted in pairs
                            matchBluetooth.add(i) 
                        listOfPersonsOthers = []
                        #Catching the upper and lower appartmens (if any)
                        if building.nFloors > 1:
                            if app.floor == 0:
                                listOfPersonsOthers = listOfPersonsOthers + building.floors[1].appartments[app.appartment].persons 
                            elif app.floor == building.nFloors - 1:
                                listOfPersonsOthers = listOfPersonsOthers + building.floors[building.nFloors-2].appartments[app.appartment].persons 
                            else:
                                listOfPersonsOthers = listOfPersonsOthers + building.floors[app.floor-1].appartments[app.appartment].persons
                                listOfPersonsOthers = listOfPersonsOthers + building.floors[app.floor+1].appartments[app.appartment].persons
                        #Catching the sides (if any)
                        if floor.nAppartments > 1:
                            for s in [-1, 0, 1]:
                                for t in [-1, 0, 1]:
                                    if abs(s*t) == 1:
                                        continue
                                    if s == 0 and t == 0:
                                        continue
                                    k = floor.existsApp(app.i + s, app.j + t)
                                    if k >= 0:
                                        listOfPersonsOthers = listOfPersonsOthers + building.floors[app.floor].appartments[k].persons 
                        listOfPersonsOthersWithBluetooth = [x for x in listOfPersonsOthers if (self.thePopulation[x].quarantine == 0 and self.thePopulation[x].bluetoothOn != 0)]
                        for i in itertools.product(listOfPersonsWithBluetooth, listOfPersonsOthersWithBluetooth):
                            x1 = self.thePopulation[i[0]].x
                            x2 = self.thePopulation[i[1]].x
                            y1 = self.thePopulation[i[0]].y
                            y2 = self.thePopulation[i[1]].y
                            z1 = self.thePopulation[i[0]].z
                            z2 = self.thePopulation[i[1]].z
                            if math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) + (z1-z2)*(z1-z2)) > self.conf.bluetoothRadius:
                                continue 
                            #This is called to put only once this contact because the other will come later 
                            matchBluetooth2.add(i) 
 
        #Going for infections
        for i in matchInfection:
            self.infect(i[0], i[1])
                        
        #Going for bluetooth contact
        if self.conf.strategy > 2:
            for i in matchBluetooth:
                self.bluetooth(i[0], i[1])
            for i in matchBluetooth2:
                self.bluetooth2(i[0], i[1])
                        
    ###################################################################################################
    ###################################################################################################
    def infect(self, person1, person2):
        dice = random.random()
        if dice < self.conf.instantInfectionProbability:
            #print('Infection between ' + str(person1) + ' ' + str(person2))
            if self.thePopulation[person1].health == 1:
                self.thePopulation[person2].infect(self.time)
                #print('Person: ' + str(person1) + ' infected person: ' + str(person2))
            else:
                self.thePopulation[person1].infect(self.time)
                #print('Person: ' + str(person2) + ' infected person: ' + str(person1))

    ###################################################################################################
    ###################################################################################################
    def bluetooth(self, person1, person2):
   
        #if self.thePopulation[person1].quarantine == 1 or self.thePopulation[person2].quarantine == 1:
        #    return
        #if self.thePopulation[person1].bluetoothOn== 0 or self.thePopulation[person2].bluetoothOn==0:
        #    return
        self.thePopulation[person1].bluetoothMatch(person2, self.thePopulation[person1].x, self.thePopulation[person1].y, self.time)
        self.thePopulation[person2].bluetoothMatch(person1, self.thePopulation[person2].x, self.thePopulation[person2].y, self.time)

    ###################################################################################################
    ###################################################################################################
    def infect2(self, person1, person2):
        dice = random.random()
        if dice < self.conf.instantInfectionProbability:
            self.thePopulation[person1].infect(self.time)
            #print('Person: ' + str(person2) + ' infected person: ' + str(person1))

    ###################################################################################################
    ###################################################################################################
    def bluetooth2(self, person1, person2):
   
        #if self.thePopulation[person1].quarantine == 1 or self.thePopulation[person2].quarantine == 1:
        #    return
        #if self.thePopulation[person1].bluetoothOn== 0 or self.thePopulation[person2].bluetoothOn==0:
        #    return
        #self.thePopulation[person1].bluetoothMatch(person2, self.thePopulation[person1].x, self.thePopulation[person1].y, self.time)
        self.thePopulation[person1].bluetoothMatch(person2, self.thePopulation[person1].x, self.thePopulation[person1].y, self.time)

    ###################################################################################################
    ###################################################################################################
    def clearBluetooth(self):

        for i in self.thePopulation:
            i.bluetoothmatches.clear()

    ###################################################################################################
    ###################################################################################################
    def update(self):

        #For each person
        for i in self.thePopulation:
            #If healthy -> update
            if i.health == 0:
                i.health = i.newHealth
                #if i.newHealth == 1:
                #    self.fileToSave.write('Infected ' + str(i.person) + ' ' + str(self.time) + '\n') 
            #If infected
            if i.health == 1 :
                #If cured
                if self.time > i.timeOfCuration:
                    i.health = 2
                    i.symptoms = 0
                    i.quarantine = 0 
                    i.canInfect = 0
                    #self.fileToSave.write('Cured ' + str(i.person) + ' ' + str(self.time) + '\n') 
                #If presenting symptoms
                elif self.time > i.timeOfIncubation:
                    if i.hasSymptoms and not i.symptoms:
                        i.symptoms = 1
                        i.quarantine = 1
                #If passed infection time
                elif self.time > i.timeToInfect:
                    i.canInfect = 1
            
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
        person.newposition = 1
        person.howlongcounter = 0
        person.howlong = int(round(random.gammavariate(self.conf.timescalehome, 1)))

    ###################################################################################################
    ###################################################################################################
    def runHome(self, person):

        person.howlongcounter = person.howlongcounter + 1
        if person.howlongcounter >= person.howlong:
            [person.x, person.y] = self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].GetRandomPosition()
            person.newposition = 1
            person.howlongcounter = 0
            person.howlong = int(round(random.gammavariate(self.conf.timescalehome, 1)))

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
        person.newposition = 1
        person.howlongcounter = 0
        person.howlong = int(round(random.gammavariate(self.conf.timescalework, 1)))

    ###################################################################################################
    ###################################################################################################
    def runWork(self, person):

        person.howlongcounter = person.howlongcounter + 1
        if person.howlongcounter >= person.howlong:
            [person.x, person.y] = self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].GetRandomPosition()
            person.newposition = 1
            person.howlongcounter = 0
            person.howlong = int(round(random.gammavariate(self.conf.timescalework, 1)))

    ###################################################################################################
    ###################################################################################################
    def goLeisure(self, person):

        self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].removePerson(person.person)  
        person.lastposition = 2
        person.leisurehowlong = int(round(random.gammavariate(self.conf.timescaleleisuresite, 1)))
        person.leisurehowlongcounter = 0
        person.activeBuilding = self.buildings[self.leisureBuildingIndexes[random.randint(0, self.conf.nLeisureBuildings-1)]].building
        person.activeFloor = 0
        person.activeAppartment = random.randint(0, self.buildings[person.activeBuilding].floors[0].nAppartments-1)
        self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].addPerson(person.person)
        [person.x, person.y] = self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].GetRandomPosition()
        person.newposition = 1
        person.howlongcounter = 0
        person.howlong = int(round(random.gammavariate(self.conf.timescaleleisure, 1)))


    ###################################################################################################
    ###################################################################################################
    def runLeisure(self, person):
        
        person.howlongcounter = person.howlongcounter + 1
        person.leisurehowlongcounter = person.leisurehowlongcounter + 1
        if person.leisurehowlongcounter >= person.leisurehowlong:
            person.leisurehowlong = int(round(random.gammavariate(self.conf.timescaleleisuresite, 1)))
            person.leisurehowlongcounter = 0 
            self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].removePerson(person.person)  
            person.activeBuilding = self.buildings[self.leisureBuildingIndexes[random.randint(0, self.conf.nLeisureBuildings-1)]].building
            person.activeFloor = 0
            person.activeAppartment = random.randint(0, self.buildings[person.activeBuilding].floors[0].nAppartments-1)
            self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].addPerson(person.person)
            [person.x, person.y] = self.buildings[person.activeBuilding].floors[person.activeFloor].appartments[person.activeAppartment].GetRandomPosition()
            person.newposition = 1
            person.howlongcounter = 0
            person.howlong = int(round(random.gammavariate(self.conf.timescaleleisure, 1)))
 
        if person.howlongcounter >= person.howlong:
            [person.x, person.y] = self.buildings[person.activeBuilding].floors[0].appartments[person.activeAppartment].GetRandomPosition()
            person.newposition = 1
            person.howlongcounter = 0
            person.howlong = int(round(random.gammavariate(self.conf.timescaleleisure, 1)))
        
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

        self.nQuarantine = 0
        self.nHealthy = 0
        self.nCured = 0
        self.nInfected = 0
        for i in self.thePopulation:
            if i.quarantine == 1:
                self.nQuarantine = self.nQuarantine + 1
            if i.health == 0:
                self.nHealthy = self.nHealthy + 1
            elif i.health == 1:
                self.nInfected = self.nInfected + 1
            else:
                self.nCured = self.nCured + 1

        print('----------------Stats--------------------')
        print('Day: ', str(day))
        print('Number of healthy people: ' + str(self.nHealthy) + ', number of infected people: ' + str(self.nInfected) + ', number of cured people: ' + str(self.nCured) + " and  number of people in quarantine: ", self.nQuarantine)  
        self.days.append(day)
        self.healthy.append(self.nHealthy)
        self.infected.append(self.nInfected)
        self.cured.append(self.nCured)
        self.nquarantine.append(self.nQuarantine)
    ####################################################################################################
    ###################################################################################################
    def Save(self):

        thelist = [self.days, self.healthy, self.infected, self.cured, self.nquarantine]
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
        newtime = self.time - days * (24.0*60)
        hour = math.floor(newtime / 60)
        return hour

    ###################################################################################################
    ###################################################################################################
    def storeGeometricInfo(self):

        self.fileToSave.write(str(self.time) + '\n')
        for person in self.thePopulation:
            self.fileToSave.write(str(person.health) + ' ' + str(person.quarantine) + ' ' + str(person.x) + ' ' + str(person.y) + '\n')

