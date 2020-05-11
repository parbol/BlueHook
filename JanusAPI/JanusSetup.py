###############################################################
#Python-based application to communicate with the Janus server#
#Requires the gremlinpython API                               #
#sudo pip install gremlinpython==3.4.6                        #
###############################################################
from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.driver.client import Client




class JanusSetup:

    def __init__(self, serverlocation, mode):

        self.serverlocation = serverlocation
        self.client = Client(serverlocation, 'g')
        if mode == 0:
            self.schema_msg = """
                mgmt = graph.openManagement()
                nameid = mgmt.makePropertyKey('nameid').dataType(String.class).cardinality(SINGLE).make()
                state = mgmt.makePropertyKey('state').dataType(Integer.class).cardinality(SINGLE).make()
                firstlogin = mgmt.makePropertyKey('firstlogin').dataType(Integer.class).cardinality(SINGLE).make()
                infectiondate = mgmt.makePropertyKey('infectiondate').dataType(Integer.class).cardinality(SINGLE).make()
                curationdate = mgmt.makePropertyKey('curationdate').dataType(Integer.class).cardinality(SINGLE).make()
                time = mgmt.makePropertyKey('time').dataType(Integer.class).cardinality(SINGLE).make()
                duration = mgmt.makePropertyKey('duration').dataType(Integer.class).cardinality(SINGLE).make()
                hlocation = mgmt.makePropertyKey('hlocation').dataType(Double.class).cardinality(SINGLE).make()
                vlocation = mgmt.makePropertyKey('vlocation').dataType(Double.class).cardinality(SINGLE).make()
                incontact = mgmt.makeEdgeLabel('incontactwith').multiplicity(MULTI).make()
                mgmt.commit()"""
        else:
            self.schema_msg = 'graph.io(IoCore.graphml()).writeGraph("graph.xml")'
        self.client.submit(self.schema_msg)







