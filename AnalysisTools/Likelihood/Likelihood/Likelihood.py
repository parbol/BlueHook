from Likelihood.Reader import Reader

import math




###############################################################
###############################################################
class Likelihood:

    def __init__(self, reader):
        
        self.reader = reader

    
    ###############################################################
    ###############################################################
    def probabilityHealthy(self, i, p):
    
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
        print(suma)
        return 1.0 - math.pow(p, suma)

    ###############################################################
    ###############################################################
    def q(self, p):
        qv = 0
        for i in range(0, self.reader.npersons):
            ps = self.probabilityHealthy(i, p)
            if ps == 1:
                continue
            if self.reader.status[i] == 0:
                qv = qv - 2.0 * math.log( ps )
            else:
                qv = qv - 2.0 * math.log(1.0 - ps)
        return qv

