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
            val = self.reader.eta(i, k)
            #print('Person ' + str(i) + ' time in contact with ' + str(k) + ' ' + str(val))
            suma = suma + val
        return suma

    ###############################################################
    ###############################################################
    def q(self, p):
        qv = 0
        for i in range(0, self.reader.npersons):
            if i == 0:
                continue
            psum = self.giveSum(i)
            #print(psum)
            #if psum == 0:
            #    continue
            if self.reader.status[i] == 0:
                #print('Adding in 0 ', str(2.0 * psum * math.log(1.0-p)))
                qv = qv - 2.0 * psum * math.log(1.0 - p)
            else:
                #if psum == 0:
                #    psum = 1
                #print('Adding in 1 ', str(2.0 * math.log(1.0 - math.pow(1.0-p, psum))))
                qv = qv - 2.0 * math.log(1.0 - math.pow(1.0-p, psum))
        return qv

