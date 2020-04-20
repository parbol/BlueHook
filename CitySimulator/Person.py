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


    def Print(self):

        print('---------------------------------------------------')
        print('|            Person  parameters                   |')
        print('---------------------------------------------------')
        print('Id: ' + self.theId)
        print('Person index: ' + str(self.person))
        print('Living in building: ' + str(self.building) + ', floor: ' + str(self.floor) + ', appartment: ', str(self.appartment))
        print('Working in building: ' + str(self.workplace) + ', floor: ' + str(self.floorWorkplace) + ', appartment: ', str(self.appartmentWorkplace))




    

