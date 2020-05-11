from optparse import OptionParser
import os
import stat
import pandas as pd
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patches as patches
import glob
import math

if __name__ == "__main__":


    arr = np.genfromtxt('datos.txt', delimiter=' ')
    fig = plt.figure()
    plt.plot(arr[:,0], arr[:,1])
    plt.title('Probability estimation')
    plt.xlabel('p')
    plt.ylabel('q = -2 log(L)')
    plt.axvline(x=0.0017, color='red')
    plt.savefig('likelihood.png')
    plt.show()





