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
    likelihood = Likelihood(reader)

    p = [0.07, 0.0035059, 0.001]
    for s in p:
        print(likelihood.q(s))




