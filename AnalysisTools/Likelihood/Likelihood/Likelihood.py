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
            #print(i, k, self.reader.eta(i,k))
            suma = suma + self.reader.eta(i, k)
        return suma

    ###############################################################
    ###############################################################
    def q(self, p):
        qv = 0
        for i in range(0, self.reader.npersons):
            psum = self.giveSum(i)
            #print(psum)
            if psum == 0:
                continue
            if self.reader.status[i] == 0:
                qv = qv - 2.0 * psum * math.log(1.0 - p)
            else:
                qv = qv - 2.0 * math.log(1.0 - math.pow(1.0-p, psum))
        return qv

