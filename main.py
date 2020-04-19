from JanusAPI import JanusServer
from JanusAPI.Match import Match
from JanusAPI.User import User

import datetime



if __name__ == "__main__":

    myapi = JanusServer.JanusServer('ws://localhost:8182/gremlin')

    user1 = User('id1', 'non-infected', datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now())   
    user2 = User('id2', 'non-infected', datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now())   
    match = Match(user1, user2, [1, 2], datetime.datetime.now(), 20)
    myapi.insertMatch(match)


 

