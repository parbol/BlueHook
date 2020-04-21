###############################################################
#Python-based application for handling a Floor                #
###############################################################

from CitySimulator.Appartment import Appartment
import math

class Floor:

    def __init__(self, buildingId, floorId, conf, x, y, nAppartments):

        self.building = buildingId
        self.floor = floorId
        self.lFloor = conf.lBuilding
        self.x = x
        self.y = y
        self.nAppartmentsPerSide = math.floor(math.sqrt(nAppartments))
        self.nAppartments =  self.nAppartmentsPerSide * self.nAppartmentsPerSide 
        self.appartments = []
        self.lAppartment = conf.lBuilding/self.nAppartments

        for i in range(0, self.nAppartmentsPerSide):
            for j in range(0, self.nAppartmentsPerSide):
                index = i * self.nAppartmentsPerSide + j
                theX = (x - self.lFloor / 2.0) + i * self.lAppartment + self.lAppartment/2.0
                theY = (y - self.lFloor / 2.0) + j * self.lAppartment + self.lAppartment/2.0
                app = Appartment(self.building, self.floor, index, conf, theX, theY, self.lAppartment)
                self.appartments.append(app)

    def Print(self):

        print('---------------------------------------------------')
        print('|              Floor parameters                   |')
        print('---------------------------------------------------')
        print('Building Id: ' + str(self.building))
        print('Id: ' + str(self.floor))
        print('Location: (' + str(self.x) + ', ' + str(self.y) + ')')
        print('Number of Appartments: ' + str(self.nAppartments))
        for app in self.appartments:
            app.Print()

    

