###############################################################
#Python-based application for handling a CDC                  #
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
class CDC:

    def __init__(self, thePopulation, buildings, conf):
        

        self.thePopulation = thePopulation
        self.buildings = buildings
        self.conf = conf
        self.tested = []
        self.time = 0
        self.numberOfTests = 0
        self.numberOfTestsPositive = 0

    ###################################################################################################
    ###################################################################################################
    def suspiciousFamilies(self):

        totalSuspiciousFamilies = set()
        #For each person
        randomPopulation = random.sample(self.thePopulation, k=self.conf.realPopulation)
        for i in randomPopulation:
            if i.familyTested == True:
                continue
            if i.quarantine==1 and (self.time - i.quarantineTime) < 7200:
                for x in self.buildings[i.residentialBuilding].floors[i.residentialFloor].appartments[i.residentialAppartment].inhabitants:
                    if x == i.person:
                        continue
                    if x not in self.tested and self.thePopulation[x].quarantine!=1 and self.thePopulation[x].health !=2 and (self.time - self.thePopulation[x].lastTestTime) > 7200:
                        i.familyTested = True
                        totalSuspiciousFamilies.add(x)
                        if(len(totalSuspiciousFamilies) == self.conf.numberOfTestsPerDay):
                            return(totalSuspiciousFamilies)
        return(totalSuspiciousFamilies)

    ###################################################################################################
    ###################################################################################################
    def suspiciousBluetoothMatchesWithTime(self):
                

        mydict = dict()
        for i in self.thePopulation:
            if i.quarantine==1 and (self.time - i.quarantineTime) < 7200:
                thebluetooth = i.bluetoothOldMatches + i.bluetoothmatches
                for j in thebluetooth:
                    x = j[0]
                    if not (x not in self.tested and self.thePopulation[x].quarantine!=1 and self.thePopulation[x].health!=2 and (self.time - self.thePopulation[x].lastTestTime) > 7200):
                        continue
                    if (self.time - j[3]) < self.conf.bluetoothTimeRange and j[4] >= self.conf.minBluetoothTime:
                        if j[0] in mydict:
                            mydict[j[0]] += j[4]
                        else:
                            mydict[j[0]] = j[4]
        totalSuspiciousMatches = []
        k = sorted(mydict.items(), key=lambda x: x[1], reverse=True)
        for c in k:
            totalSuspiciousMatches.append(c[0])

        return(totalSuspiciousMatches)


    ###################################################################################################
    ###################################################################################################
    def suspiciousBluetoothMatches(self):

        totalSuspiciousMatches=[]
        for i in self.thePopulation:
            suspiciousMatches=[]
            if self.conf.strategy==4:
                if i.symptoms==1:
                    thebluetooth = i.bluetoothOldMatches + i.bluetoothmatches
                    for j in thebluetooth:
                        if (self.time - j[3]) < self.conf.bluetoothTimeRange and j[4] >= self.conf.minBluetoothTime:
                            suspiciousMatches.append(j[0])
                totalSuspiciousMatches+=suspiciousMatches

            if self.conf.strategy == 5:
                if i.symptoms==1 or i.positiveTested==1:
                #List with people bluetooth matched
                #print('Person ' + str(i.person) + ' in quarantine')
                #print('Contacts of person are: ')
                #print(i.bluetoothOldMatches)
                    thebluetooth = i.bluetoothOldMatches + i.bluetoothmatches
                    for j in thebluetooth:
                        x = j[0]
                        if not (x not in self.tested and self.thePopulation[x].symptoms==0 and self.thePopulation[x].health!=2 and (self.time - self.thePopulation[x].lastTestTime) > 7200):
                            continue
                        if (self.time - j[3]) < self.conf.bluetoothTimeRange and j[4] >= self.conf.minBluetoothTime:
                            suspiciousMatches.append(j[0])
                totalSuspiciousMatches+=suspiciousMatches

        return(set(totalSuspiciousMatches))


    ###################################################################################################
    ###################################################################################################
    def Testing(self, dailyTested):

        for i in dailyTested:
            #print('Testing: ', i)
            #resb = self.thePopulation[i].residentialBuilding
            #resf = self.thePopulation[i].residentialFloor
            #resa = self.thePopulation[i].residentialAppartment
            self.numberOfTests += 1
            citizen=self.thePopulation[i]
            citizen.lastTestTime = self.time
            if citizen.health == 1:
                self.numberOfTestsPositive += 1
                citizen.quarantine = 1
                citizen.quarantineTime=self.time
                citizen.positiveTested=1
                self.tested.append(i)
            elif citizen.health == 0 and self.conf.strategy == 5:
                if citizen.quarantine ==1:
                    citizen.quarantine = 0
                    citizen.quarantineTime = 0

    ###################################################################################################
    ###################################################################################################
    def printInfoPerson(self, index):
       
        person = self.thePopulation[index]
        b = person.residentialBuilding
        f = person.residentialFloor
        a = person.residentialAppartment
        text1 = 'Person ' + str(index) + ' State: ' + str(person.health) + ' Quarantine: ' + str(person.quarantine) + ' Symptomatic: ' + str(person.hasSymptoms) + ' Symptoms: ' + str(person.symptoms) + ' Last test time ' + str(person.lastTestTime)
        text2 = 'Living with: '  
        for i in self.buildings[b].floors[f].appartments[a].inhabitants:
            if i == person.person:
                continue
            text2 += str(i) + ' '
        text3 = 'Bluetooth matches: '
        myset = set() 
        for i in person.bluetoothmatches + person.bluetoothOldMatches:
            myset.add(i[0])
        for i in myset:
            text3 += str(i) + ' '
        print(text1)
        print(text2)
        print(text3)

    ###################################################################################################
    ###################################################################################################
    def debugingPopulation(self):

        print('@@@@@@@@@@@@@@@@@@Debugging the population@@@@@@@@@@@@@@@@@@@@@@@@')
        for i in self.thePopulation:
            self.printInfoPerson(i.person)

    ###################################################################################################
    ###################################################################################################
    def runTestStrategy1(self):

                 
        notYetTested=[x for x in range(self.conf.realPopulation) if x not in self.tested and self.thePopulation[x].quarantine!=1 and self.thePopulation[x].health !=2 and (self.time - self.thePopulation[x].lastTestTime) > 7200]
        if len(notYetTested) >= self.conf.numberOfTestsPerDay:
            dailyTested=random.sample(notYetTested, k=self.conf.numberOfTestsPerDay)
        else:
            dailyTested=notYetTested

        self.Testing(dailyTested)

 
    ###################################################################################################
    ###################################################################################################
    def runTestStrategy2(self):
        
            
        notYetTested = [x for x in self.suspiciousFamilies()]
        if len(notYetTested) >= self.conf.numberOfTestsPerDay:
            dailyTested=notYetTested[:self.conf.numberOfTestsPerDay]
        else:
            dailyTested=notYetTested

        self.Testing(dailyTested)


    ###################################################################################################
    ###################################################################################################
    def runTestStrategy3(self):
        
        notYetTested=[x for x in self.suspiciousBluetoothMatchesWithTime()]
        if len(notYetTested) >= self.conf.numberOfTestsPerDay:
            dailyTested=notYetTested[0:self.conf.numberOfTestsPerDay]
        else:
            dailyTested=notYetTested

        self.Testing(dailyTested)

    ###################################################################################################
    ###################################################################################################
    def runTestStrategy4(self):

        notYetTested=[x for x in self.suspiciousBluetoothMatches() if self.thePopulation[x].quarantine!=1 and self.thePopulation[x].health!=2]
        dailyTested=notYetTested
        for i in dailyTested:
            citizen=self.thePopulation[i]
            citizen.quarantine = 1
            citizen.quarantineTime=self.time


    ###################################################################################################
    ###################################################################################################
    def runTestStrategy5(self):
        
        notYetTested=[x for x in self.suspiciousBluetoothMatches()]
        if len(notYetTested) >= self.conf.numberOfTestsPerDay:
            dailyTested=random.sample(notYetTested, k=self.conf.numberOfTestsPerDay)
        else:
            dailyTested=notYetTested
        
        self.Testing(dailyTested)

        dailyQuarantined=[x for x in notYetTested if x not in dailyTested]
        for i in dailyQuarantined:
            self.thePopulation[i].quarantine = 1
            self.thePopulation[i].quarantineTime = self.time


    ###################################################################################################
    ###################################################################################################
    def runTests(self, time, day):

        self.time = time
        strategy=self.conf.strategy
        #No testing - strategy 0
        if (strategy==0):
            return

        #Random testing - strategy 1
        if (strategy==1):
            self.runTestStrategy1()

        #Testing families - strategy 2
        if (strategy==2):
            self.runTestStrategy2()

        #Testing bluetooth matches - strategy 3
        if (strategy ==3):
            self.runTestStrategy3()
        
        #Putting in quarantine all the bluetooth matches - strategy 4
        if (strategy ==4):
            self.runTestStrategy4()

        #Testing bluetooth matches and sending the no tested to quarantine - strategy 5
        if (strategy == 5):
            self.runTestStrategy5()


