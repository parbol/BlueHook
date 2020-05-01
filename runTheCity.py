from CitySimulator.City import City
from optparse import OptionParser




if __name__ == "__main__":


    parser = OptionParser(usage="%prog --help")
    parser.add_option("-o", "--output",    dest="output",       type="string",   default='output.csv', help="Name of the output file")
    parser.add_option("-s", "--seed",      dest="seed",         type="int",      default='1',          help="Seed")
    parser.add_option("-c", "--config",    dest="config",       type="string",   default='1',          help="Config file")
    parser.add_option("-m", "--mode",      dest="mode",         type="int",      default='1',          help="Mode: 0 with database, 1 without database")
    parser.add_option("-d", "--days",      dest="days",         type="int",      default='20',         help="Number of days to run")
    (options, args) = parser.parse_args()


    city = City(options.config, 'ws://localhost:8182/gremlin', options.output, options.seed, options.mode)
    city.runDays(options.days)



 

