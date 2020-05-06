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


    print(reader.infected[4])

    likelihood = Likelihood(reader)

    p = [0.5, 0.4, 0.3, 0.2, 0.1, 0.01, 0.008, 0.006, 0.004, 0.003, 0.002, 0.001, 0.0005, 0.0001]
    for s in p:
        print(s, likelihood.q(s))




