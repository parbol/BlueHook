###############################################################
#Class encapsulating the contact of two bluettooth deviced    #
###############################################################
import datetime
from JanusAPI.User import User


class Match:

    def __init__(self, user1, user2index, location, time, duration):

        self.user1 = user1
        self.user2 = 'user_' + str(user2index)
        self.hlocation = location[0]
        self.vlocation = location[1]
        self.time = time
        self.duration = duration
        
    def Print(self)
        print('----------------------Match---------------------')
        print('Id1 :', self.user1)
        self.user1.Print()
        print('Id2 :', self.user2)
        print('Location: ', '(' + str(self.hlocation) + ', ' + str(self.vlocation) + ')')
        print('Time: ', str(self.time))
        print('Duration: ', str(self.duration))


