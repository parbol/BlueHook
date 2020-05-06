from optparse import OptionParser
import math





###############################################################
###############################################################
class City:

    def __init__(self, fileName, npersons):
        
    self.infected = []
    self.status = []
    self.contacts = dict()
    self.filename = filename
    self.npersons = npersons
    self.f = open(fileName)


    def readInfected(self):

        for i in range(0, self.npersons):
            self.infected.append([-1, -1])
                
        for i in self.f.readlines():
            s = i.split()
            if s[0] == 'Infected':
                id1 = int(s[1])
                time = int(s[2])
                infected[id1][0] = time
            if s[0] == 'Cured':
                id1 = int(s[1])
                time = int(s[2])
                infected[id1][1] = time

        return infected

    def readContacts(self):

        for i in f.readlines():
            s = i.split()
            if s[0] == 'Contact':
                id1 = int(s[1])
                id2 = int(s[2])
                time = int(s[3])
                if time == self.lt:
                    break
                c = (id1, time)
                if c not in contacts.keys():
                    v = []
                    v.append(id2)
                    contacts[c] = v
                else:
                    self.contacts[c].append(id2)


    def eta(contacts, i, j, t):
    c = (i, t)
    if c in contacts.keys() and j in contacts[c]:
        return 1
    return 0


def delta(infected, i, t):
    if infected[i][0] == -1:
        return 0
    else:
        if infected[i][0] <= t and (infected[i][1] == -1 or infected[i][1] >= t):
            return 1
    return 0


def lastTime(filename):

    f = open(filename)
    t = 0
    for i in f.readlines():
        if i.split()[0] == 'Infected':
            time = int(i.split()[2])
        if i.split()[0] == 'Cured':
            time = int(i.split()[2])
        if time > t:
            t = time
    return t

def status(t, n):

    status = []
    for i in range(0, n):
        status.append(delta(i, t))
    return status
    


def probability(contacts, infected, p, i, lt):
    
    suma = 0
    for k, j in enumerate(infected):
        if k == i:
            continue
        tmin = j[0]
        tmax = j[1]
        if tmin == -1:
            continue
        if tmax == -1:
            tmax = lt
        for n in range(tmin, tmax):
             if eta(contacts, i, k, n):
                 suma = suma + 1

    return math.pow(p, suma)


if __name__ == "__main__":


    parser = OptionParser(usage="%prog --help")
    parser.add_option("-i", "--input",    dest="inputFile",       type="string",   default='geometry.txt', help="File name.")
    parser.add_option("-n", "--number",   dest="n",               type="int",      default=470,            help="N users")
    (options, args) = parser.parse_args()
   
    lt = lastTime(options.inputFile)
    contacts = readContacts(options.inputFile, options.n, lt)
    infected = readInfected(options.inputFile, options.n)
    thestatus = status(lt, options.n)

    print('Ready to go')

    prob = [0.003]
    q = 0
    for p in prob:
        for i in range(0, options.n):
            ps = probability(contacts, infected, p, i, lt)
            q = q - 2 * log((1-thestatus[i]) * ps + thestatus[i] * (1 - ps))
     
    
    print(q)



