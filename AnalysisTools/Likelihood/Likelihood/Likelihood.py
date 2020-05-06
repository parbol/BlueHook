from Likelihood.Reader import Reader

import math




###############################################################
###############################################################
class Likelihood:

    def __init__(self, reader):
        
        self.reader = reader

    
    ###############################################################
    ###############################################################
    def giveSum(self, i):
    
        suma = 0
        for k, j in enumerate(self.reader.infected):
            if k == i:
                continue
            tmin = j[0]
            tmax = j[1]
            if tmin == -1:
                continue
            if tmax == -1:
                tmax = self.reader.lt
            for n in range(tmin, tmax):
                if self.reader.eta(i, k, n):
                    suma = suma + 1
        return suma

    ###############################################################
    ###############################################################
    def q(self, p):
        qv = 0
        for i in range(0, self.reader.npersons):
            psum = self.giveSum(i)
            if psum == 0:
                continue
            if self.reader.status[i] == 0:
                qv = qv - 2.0 * psum * (1 - p)
            else:
                qv = qv - 2.0 * math.log(1.0 - math.pow(1-p, psum))
        return qv

