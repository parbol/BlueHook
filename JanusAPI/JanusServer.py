###############################################################
#Python-based application to communicate with the Janus server#
#Requires the gremlinpython API                               #
#sudo pip install gremlinpython==3.4.6                        #
###############################################################
#from gremlin_python import statics
#from gremlin_python.structure.graph import Graph
#from gremlin_python.process.graph_traversal import __
#from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection


from JanusAPI.Match import Match 
from JanusAPI.User import User



class JanusServer:

    def __init__(self, serverlocation):

        self.serverlocation = serverlocation
        #self.connection = DriverRemoteConnection(serverlocation, 'g')
        #self.graph = Graph()
        #self.g = self.graph.traversal().withRemote(self.connection)

    #def insertMatch(self, match):
    #
    #    user1v = self.g.V().has('nameid', match.user1.nameid).toList()
    #    user2v = self.g.V().has('nameid', match.user2.nameid).toList()
    #    if not user1v:
    #        print('Creating vertex', match.user1.nameid)
    #        self.createNewVertex(match.user1)
    #    if not user2v:
    #        print('Creating vertex', match.user2.nameid)
    #        self.createNewVertex(match.user2)
    #    self.createNewEdge(match)

    #def createNewVertex(self, user):
        
   #     self.g.addV('person').property('nameid', user.nameid).property('state',  user.state).property('firstlogin', user.firstlogin).property('infectiondate', user.infectiondate).property('curationdate', user.curationdate).iterate()


    #def createNewEdge(self, match):

     #   edge = self.g.V().has('nameid', match.user1.nameid).addE('incontactwith').to(self.g.V().has('nameid', match.user2.nameid)).next()
      #  self.g.E(edge).property('hlocation', match.hlocation).property('vlocation', match.vlocation).property('time', match.time).property('duration', match.duration).iterate()



    def insertMatchFake(self, match):

        print('Inserting the following match in the database:')
        match.Print()





