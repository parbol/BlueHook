###############################################################
#Python-based application for handling a Person               #
###############################################################


class Person:

    def __init__(self, theId, person, house, floor, appartment, workplace, floorworkplace, appartmentworkplace):

        self.theId = theId
        self.person = person
        self.residentialBuilding = house
        self.residentialFloor = floor
        self.residentialAppartment = appartment
        self.workplaceBuilding = workplace
        self.workplaceFloor = floorworkplace
        self.workplaceAppartment = appartmentworkplace
        self.activeBuilding = house
        self.activeFloor = floor
        self.activeAppartment = appartment
        #Susceptible, Infected, Cured
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
        print('Living in building: ' + str(self.residentialBuilding) + ', floor: ' + str(self.residentialFloor) + ', appartment: ', str(self.residentialAppartment))
        print('Working in building: ' + str(self.workplaceBuilding) + ', floor: ' + str(self.workplaceFloor) + ', appartment: ', str(self.workplaceAppartment))
        print('Active building: ' + str(self.activeBuilding) + ', floor: ' + str(self.activeFloor) + ', appartment: ', str(self.activeAppartment))
        print('Current state: ' + str(self.lastposition))
        print('Position is: (' + str(self.x) + ', ' + str(self.y) + ')')





    

