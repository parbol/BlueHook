###############################################################
#Python-based application for handling a building             #
###############################################################
from CitySimulator.Floor import Floor
import numpy as np

class Building:

    def __init__(self, theId, conf, i_index, j_index, theType):

        self.building = theId
        self.lBuilding = conf.lBuilding
        self.x = i_index * conf.lBlock + conf.lStreet + conf.lBuilding/2.0
        self.y = j_index * conf.lBlock + conf.lStreet + conf.lBuilding/2.0
        self.theType = theType
        self.nFloors = 1
        if theType != 2:
            self.nFloors = 1 + np.random.poisson(conf.nFloorIndex, 1)[0]
        self.nAppartmentsPerFloor = 1 + np.random.poisson(conf.nAppartmentIndex, 1)[0]

        self.floors = []
        for i in range(0, self.nFloors):
            floor = Floor(theId, i, conf, self.x, self.y, self.nAppartmentsPerFloor) 
            self.floors.append(floor)


    def Print(self):

        print('---------------------------------------------------')
        print('|            Building parameters                   |')
        print('---------------------------------------------------')
        print('Id: ' + str(self.building))
        print('Location: (' + str(self.x) + ', ' + str(self.y) + ')')
        print('Type: ' + str(self.theType))
        print('Number of floors: ' + str(self.nFloors))
        for floor in self.floors:
            floor.Print()


    

