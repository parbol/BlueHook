from optparse import OptionParser
from Likelihood.Reader import Reader
from Likelihood.Likelihood import Likelihood




###############################################################
###############################################################
if __name__ == "__main__":


    parser = OptionParser(usage="%prog --help")
    parser.add_option("-i", "--input",    dest="inputFile",       type="string",   default='geometry.txt', help="File name.")
    parser.add_option("-n", "--number",   dest="n",               type="int",      default=470,            help="N users")
    (options, args) = parser.parse_args()
   
    reader = Reader(options.inputFile, options.n)

    count = 0
    #for j, i in enumerate(reader.infected):
    #    print(j, i)
    #for i in range(0, len(reader.contacts)):
    #    for j in range(0, len(reader.contacts)):
    #        if i == j:
    #            continue
    #        print('Person ' + str(i) + ' and person ' + str(j), reader.contacts[i][j]) 
    #print(reader.infected[10])
    #print(reader.infected[20])
    #print(reader.infected[70])
    #print(reader.infected[100])
    #print(reader.infected[200])
    #print(reader.infected[300])

    likelihood = Likelihood(reader)

    p = [0.5, 0.4, 0.3, 0.2, 0.1, 0.01, 0.008, 0.006, 0.004]
    for i in range(0, 30):
        p.append(0.003 - i * 0.0001)

    for s in p:
        print(s, likelihood.q(s))




