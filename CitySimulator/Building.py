###############################################################
#Python-based application for handling a building             #
###############################################################
from CitySimulator.Floor import Floor


class Building:

    def __init__(self, theId, lBuilding, x, y, theType, nFloors, nAppartments):

        self.buildingId = theId
        self.lBuilding = lBuilding
        self.x = x
        self.y = y
        self.theType = theType
        self.nFloors = nFloors
        self.nAppartments = nAppartments
        self.floors = []
        for i in range(0, self.nFloors):
            floor = Floor(theId, i, lBuilding, x, y, nAppartments) 
            self.floors.append(floor)

    def CountFloors(self):

        return self.nFloors

    def CountAppartments(self):

        return self.nFloors * self.nAppartments

    def Print(self):

        print('---------------------------------------------------')
        print('|            Building parameters                   |')
        print('---------------------------------------------------')
        print('Id: ' + self.buildingId)
        print('Location: (' + str(self.x) + ', ' + str(self.y) + ')')
        print('Type: ' + str(self.theType))
        print('Number of floors: ' + str(self.nFloors))
        for floor in self.floors:
            floor.Print()


    

