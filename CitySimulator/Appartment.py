###############################################################
#Python-based application for handling an Appartment          #
###############################################################



class Appartment:

    def __init__(self, buildingId, floorId, appId, x, y, lAppartment):

        self.buildingId = buildingId
        self.floorId = floorId
        self.appartmentId = appId
        self.x = x
        self.y = y
        self.lAppartment = lAppartment
        self.persons = []
        self.npersons = 0

    def assignPeople(self, people):

        self.persons = people
        self.npersons = len(people)
        
    def Print(self):

        print('---------------------------------------------------')
        print('|             Apparment parameters                 |')
        print('---------------------------------------------------')
        print('Building Id: ' + str(self.buildingId))
        print('Floor Id: ' + str(self.floorId))
        print('Appartment Id: ' + str(self.appartmentId))
        print('Location: (' + str(self.x) + ', ' + str(self.y) + ')')
        print('Size of Appartments: ' + str(self.lAppartment))
        print('Number of persons: ' + str(self.npersons))    
        for personindex in self.persons:
            print('Person: ' + str(personindex))


    

