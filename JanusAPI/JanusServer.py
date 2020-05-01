###############################################################
#Python-based application to communicate with the Janus server#
#Requires the gremlinpython API                               #
#sudo pip install gremlinpython==3.4.6                        #
###############################################################




class JanusServer:

    def __init__(self, serverlocation, howtorun):
        
        self.howtorun = howtorun
        if howtorun == 0:
            from gremlin_python import statics
            from gremlin_python.structure.graph import Graph
            from gremlin_python.process.graph_traversal import __
            from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
            self.serverlocation = serverlocation
            self.connection = DriverRemoteConnection(serverlocation, 'g')
            self.graph = Graph()
            self.g = self.graph.traversal().withRemote(self.connection)

    def insertMatch(self, nameid1, nameid2, user1state, firstlogin, infectiondate, curationdate, hlocation, vlocation, time, duration):

        if self.howtorun == 1:
            return
        user1v = self.g.V().has('nameid', nameid1).toList()
        user2v = self.g.V().has('nameid', nameid2).toList()
        if not user1v:
            #print('Creating vertex', nameid1)
            self.createNewVertex(nameid1, user1state, firstlogin, infectiondate, curationdate)
        if not user2v:
            #print('Creating vertex', nameid2)
            self.createNewVertex(nameid2, -1, -1, -1, -1)
   
        edge = self.g.V().has('nameid', nameid1).addE('incontactwith').to(self.g.V().has('nameid', nameid2)).next()
        self.g.E(edge).property('hlocation', hlocation).property('vlocation', vlocation).property('time', time).property('duration', duration).iterate()


    def createNewVertex(self, user, state, firstlogin, infectiondate, curationdate):
        
        self.g.addV('person').property('nameid', user).property('state',  state).property('firstlogin', firstlogin).property('infectiondate', infectiondate).property('curationdate', curationdate).iterate()








