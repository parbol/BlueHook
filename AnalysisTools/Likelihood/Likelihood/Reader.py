from optparse import OptionParser
import math





###############################################################
###############################################################
class Reader:

    def __init__(self, fileName, npersons):
        
        self.fileName = fileName
        self.npersons = npersons
        self.lt = self.lastTime()
        self.infected = []
        self.status = []
        self.contacts = dict()
        self.readInfected()
        self.readContacts()
        self.readStatus()


    ###############################################################
    ###############################################################
    def readInfected(self):

        for i in range(0, self.npersons):
            self.infected.append([-1, -1])
                
        f = open(self.fileName)
        for i in f.readlines():
            s = i.split()
            if s[0] == 'Infected':
                id1 = int(s[1])
                time = int(s[2])
                self.infected[id1][0] = time
            if s[0] == 'Cured':
                id1 = int(s[1])
                time = int(s[2])
                self.infected[id1][1] = time
        f.close()

    ###############################################################
    ###############################################################
    def readContacts(self):

        f = open(self.fileName)
        for i in f.readlines():
            s = i.split()
            if s[0] == 'Contact':
                id1 = int(s[1])
                id2 = int(s[2])
                time = int(s[3])
                if time == self.lt:
                    break
                c = (id1, time)
                if c not in self.contacts.keys():
                    v = []
                    v.append(id2)
                    self.contacts[c] = v
                else:
                    self.contacts[c].append(id2)
        f.close()

    ###############################################################
    ###############################################################
    def eta(self, i, j, t):
        c = (i, t)
        if c in self.contacts.keys() and j in self.contacts[c]:
            return 1
        return 0

    ###############################################################
    ###############################################################
    def delta(self, i, t):
        if self.infected[i][0] == -1:
            return 0
        else:
            if self.infected[i][0] <= t and (self.infected[i][1] == -1 or self.infected[i][1] >= t):
                return 1
        return 0

    ###############################################################
    ###############################################################
    def lastTime(self):

        t = 0
        f = open(self.fileName)
        for i in f.readlines():
            if i.split()[0] == 'Infected':
                time = int(i.split()[2])
            if i.split()[0] == 'Cured':
                time = int(i.split()[2])
            if time > t:
                t = time
        f.close()
        return t

    
    ###############################################################
    ###############################################################
    def readStatus(self):

        for i in range(0, self.npersons):
            self.status.append(self.delta(i, self.lt))
    
    ###############################################################
    ###############################################################



