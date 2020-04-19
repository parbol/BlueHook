###############################################################
#Class encapsulating the contact of two bluettooth deviced    #
###############################################################
import datetime
from JanusAPI.User import User


class Match:

    def __init__(self, user1, user2, location, time, duration):

        self.user1 = user1
        self.user2 = user2
        self.hlocation = location[0]
        self.vlocation = location[1]
        self.time = time
        self.duration = duration
        

