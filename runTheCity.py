from CitySimulator.City import City
from optparse import OptionParser




if __name__ == "__main__":


    parser = OptionParser(usage="%prog --help")
    parser.add_option("-o", "--output",    dest="output",       type="string",   default='output.csv', help="Name of the output file")
    parser.add_option("-s", "--seed",      dest="seed",         type="int",  default='1',          help="Seed")
    (options, args) = parser.parse_args()


    city = City('/home/pablom/Documentos/BlueHook/CityConf.cfg', 'ws://localhost:8182/gremlin', options.output, options.seed)
    city.runDays(40)



 

