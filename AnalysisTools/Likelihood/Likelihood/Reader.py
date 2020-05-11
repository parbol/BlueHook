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
        self.contacts = []
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
       
        vk = []
        for i in range(self.npersons):
            vk.append([])
            self.contacts.append([])
            for j in range(self.npersons):
                vk[i].append([])
                self.contacts[i].append([])


        f = open(self.fileName)
        for i in f.readlines():
            s = i.split()
            if s[0] == 'Contact':
                id1 = int(s[1])
                id2 = int(s[2])
                time = int(s[3])
                if time == self.lt:
                    break
                vk[id1][id2].append(time)
                vk[id2][id1].append(time)
        f.close()
        
        for i in range(self.npersons):
            for j in range(self.npersons):
                aux = []
                last = -5
                if len(vk[i][j]) == 0:
                    continue
                notStarted = True
                v = [-1, -1]
                v[0] = vk[i][j][0]
                for t in range(1, len(vk[i][j])-1):
                    if vk[i][j][t] == vk[i][j][t-1] + 1:
                        continue
                    else:
                        v[1] = vk[i][j][t-1]
                        self.contacts[i][j].append(v)
                        v = [-1, -1]
                        v[0] = vk[i][j][t]
                if vk[i][j][len(vk[i][j])-1] != self.lt-1:
                    v[1] = vk[i][j][len(vk[i][j])-1]
                self.contacts[i][j].append(v)
                     

    ###############################################################
    ###############################################################
    def eta(self, i, j):
        
        if self.infected[j][0] == -1:
            return 0
        tmini = self.infected[j][0]
        tmaxi = self.infected[j][1]
        if tmaxi == -1:
            tmaxi = self.lt - 1
        sumMinutes = 0
        for h in self.contacts[i][j]:
            tminc = h[0]
            tmaxc = h[1]
            if tmaxc == -1:
                tmaxc = self.lt-1
            maxmin = max(tmini, tminc)
            minmax = min(tmaxi, tmaxc)
            if maxmin < minmax:
                sumMinutes = sumMinutes + minmax - maxmin
        return sumMinutes

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
        time = 0
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
            if self.infected[i][0] == -1:
                self.status.append(0)
            else:
                self.status.append(1)
 
    ###############################################################
    ###############################################################



