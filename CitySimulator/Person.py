###############################################################
#Python-based application for handling a Person               #
###############################################################


class Person:

    def __init__(self, theId, person, house, floor, appartment, workplace, floorworkplace, appartmentworkplace):

        self.theId = theId
        self.person = person
        self.building = house
        self.floor = floor
        self.appartment = appartment
        self.workplace = workplace
        self.floorWorkplace = floorworkplace
        self.appartmentWorkplace = appartmentworkplace
        self.leisurePlace = 0
        self.floorLeisurePlace = 0
        self.appartmentLeisurePlace = 0
        #Susceptible
        #Infected
        #Cured
        self.health = 0
        #Last position: 0 for home, 1 for work, 2 for leisure
        self.lastposition = 0
        self.x = 0
        self.y = 0
        self.howlongcounter = 0
        self.howlong = 0
        self.leisurehowlongcounter = 0
        self.leisurehowlong = 0

    def Print(self):

        print('---------------------------------------------------')
        print('|            Person  parameters                   |')
        print('---------------------------------------------------')
        print('Id: ' + self.theId)
        print('Person index: ' + str(self.person))
        print('Living in building: ' + str(self.building) + ', floor: ' + str(self.floor) + ', appartment: ', str(self.appartment))
        print('Working in building: ' + str(self.workplace) + ', floor: ' + str(self.floorWorkplace) + ', appartment: ', str(self.appartmentWorkplace))
        print('Current state: ' + str(self.lastposition))
        print('Position is: (' + str(self.x) + ', ' + str(self.y) + ')')





    

