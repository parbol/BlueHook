from optparse import OptionParser
import os
import stat


###########################################################################################
theExecutable = """#!/bin/bash

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /gpfs/users/parbol/CMSSW_10_5_0_pre1/src
eval `scramv1 runtime -sh`
cd /gpfs/users/parbol/BlueHook

python3 runTheCity.py --output OUTPUTFILE --config CONFIGFILE --seed SEED --seedCity SEEDCITY --mode 1 --days DAYS

"""
###########################################################################################

###########################################################################################
theCityConf = """

#Configuration file for the city
#Length of the city square edge
size CITYSIZE
#Length of the building edge
lBuilding 40
#Width of the streets
lStreet 10
#Fraction of residential buildings
fracRes 0.4
#Fraction of work buildings
fracWor 0.3
#Fraction of leisure buildings
fracLei 0.3
#Average prople per appartmen
averagePopulationPerAppartment 3
#Mean of the number of floors distribution
nFloorIndex 5
#Mean of the number of appartments per floor
nAppartmentIndex 3
#Number of leisure places every person visits
nLeisurePlacesForPerson 3
#Number of hot points in each appartment
nHotPoints 4
#Length of the individual hot point
lengthOfHotPoint 3
#Time scale of being quite at home
timescalehome 120
#Time scale of being quite at work
timescalework 60
#Time scale of being quite at home
timescaleleisure 30
#Time scale of being at a same leisure place
timescaleleisuresite 60
#Lambda of the illnes in days
curationLambda 10
#Lambda of the time you need to infect someone in days
timeToInfectLambda 2
#Lambda of the incubation in days
incubationLambda DELAY
#Bluetooth radius in meters
bluetoothRadius BLUETOOTHRADIUS
#Infection radius in meters
infectionRadius 2
#Infection probability given as probability of infecting someone being together 30 minutes
infectionProbability PROBABILITY
#Probability of no symptoms
noSymptomsProbability NOSYMPTOMS
#Strategy 0 -> no testing, 1 -> random testing, 2 -> family testing, 3 -> Bluetooth testing
strategy STRATEGY
#Number of tests that can be done per day
numberOfTestsPerDay NTESTS
#How many days take into account for the blueetooth match
bluetoothTimeRange 5
#Percentage of people engaged (with the app installed and bluetooth on)
appEngagement ENGAGEMENT
#Minimal time to take bluetooth contact into consideration (in minutes)
minBluetoothTime 10

"""
###########################################################################################




def makeTag(thefile, tag, citysize, strategy, test, engagement, lbluetooth, asympton, prob, nseed, nseedcity, delay):

    
    directoryName = os.getcwd() + '/' + tag
    os.mkdir(directoryName)
    for seedCity in range(0, nseedcity):
        for seed in range(0, nseed):
                    
            confFileName = directoryName + '/confFile_' + tag + '.cfg'
            outputFileName = directoryName + '/output_' + tag + '_seed' + str(seed) + '_CitySeed' + str(seedCity) + '.csv'
            logFileName = directoryName + '/log_' + tag + '_seed' + str(seed) + '_CitySeed' + str(seedCity) + '.log'
            errFileName = directoryName + '/err_' + tag + '_seed' + str(seed) + '_CitySeed' + str(seedCity) + '.err'
            executableName = directoryName + '/run_' + tag + '_seed' + str(seed) + '_CitySeed' + str(seedCity) + '.sh'

            myCityConf = theCityConf
            myCityConf = myCityConf.replace('CITYSIZE', citysize)                 
            myCityConf = myCityConf.replace('STRATEGY', str(strategy))                 
            myCityConf = myCityConf.replace('NTESTS', test)                 
            myCityConf = myCityConf.replace('ENGAGEMENT', engagement)                 
            myCityConf = myCityConf.replace('BLUETOOTHRADIUS', lbluetooth)                 
            myCityConf = myCityConf.replace('NOSYMPTOMS', asympton)                 
            myCityConf = myCityConf.replace('PROBABILITY', prob)                 
            myCityConf = myCityConf.replace('DELAY', delay)                 
            fconf = open(confFileName, 'w')
            fconf.write(myCityConf)
            fconf.close()

            text = theExecutable
            text = text.replace('OUTPUTFILE', outputFileName)      
            text = text.replace('CONFIGFILE', confFileName)      
            text = text.replace('SEEDCITY', str(seedCity))      
            text = text.replace('SEED', str(seed))      
            text = text.replace('DAYS', str(options.days))      
            fexe = open(executableName, 'w')
            fexe.write(text)
            fexe.close()
            st = os.stat(executableName)
            os.chmod(executableName, st.st_mode | stat.S_IEXEC)
            addendum = 'sbatch ' + ' -o ' + logFileName + ' -e ' + errFileName + ' --qos=gridui_sort --partition=cloudcms ' + executableName + '\n'
            thefile.write(addendum)




if __name__ == "__main__":


    parser = OptionParser(usage="%prog --help")
    
    parser.add_option("-c", "--citysize",      dest="citysize",         type="string",      default='500',          help="Size of the city")
    parser.add_option("-s", "--strategy",      dest="strategy",         type="string",      default='1',            help="Strategies to follow.")
    parser.add_option("-t", "--test",          dest="tests",            type="string",      default='100',          help="Test capacity.")
    parser.add_option("-N", "--seedCity",      dest="nseedcity",        type="int",         default='1',            help="Seed for the city.")
    parser.add_option("-n", "--nseed",         dest="nseed",            type="int",         default='100',          help="Number of seeds per case.")
    parser.add_option("-d", "--days",          dest="days",             type="int",         default='20',           help="Number of days.")
    parser.add_option("-e", "--engagemenet",   dest="engagement",       type="string",      default='100',          help="Fraction of people with bluetooth")
    parser.add_option("-b", "--bluetooth",     dest="lbluetooth",       type="string",      default='3.0',          help="Bluetooth length")
    parser.add_option("-a", "--asymptoms",     dest="asymptoms",        type="string",      default='0.3',          help="Fraction of asymptomatic")
    parser.add_option("-p", "--probability",   dest="probability",      type="string",      default='0.1',          help="Probability")
    parser.add_option("-D", "--delay",         dest="delay",            type="string",      default='4',            help="Delay to symptoms")


    (options, args) = parser.parse_args()

    citySizes = options.citysize.split(',')
    strategies = options.strategy.split(',')
    tests = options.tests.split(',')
    engagements = options.engagement.split(',')
    lbluetooths = options.lbluetooth.split(',')
    asymptoms = options.asymptoms.split(',')
    probability = options.probability.split(',')
    delays = options.delay.split(',')

    runfile = open('toRun.sh', 'w')


    for theStrategyk in strategies:
        theStrategy = int(theStrategyk)
        if theStrategy == 0:
            for theCitySize in citySizes:
                for delay in delays:
                    for prob in probability:
                        for theAsymp in asymptoms:
                            tag = 'City_' + str(theCitySize) + '_strategy0' + '_probability' + prob + '_asymp' + str(theAsymp) + '_delay' + delay
                            makeTag(runfile, tag, theCitySize, theStrategy, tests[0], engagements[0], lbluetooths[0], theAsymp, prob, options.nseed, options.nseedcity, delay)
        elif theStrategy == 1 or theStrategy == 2:
            for theCitySize in citySizes:
                for delay in delays:
                    for prob in probability:
                        for theTest in tests:
                            for theAsymp in asymptoms:
                                tag = 'City_' + str(theCitySize) + '_strategy' + str(theStrategy) + '_probability' + prob + '_testing' + str(theTest) + '_asymp' + str(theAsymp) + '_delay' + delay
                                makeTag(runfile, tag, theCitySize, theStrategy, theTest, engagements[0], lbluetooths[0], theAsymp, prob, options.nseed, options.nseedcity, delay)
        elif theStrategy == 3 or theStrategy == 5 or theStrategy == 6:
            for theCitySize in citySizes:
                for delay in delays:
                    for prob in probability:
                        for theTest in tests:
                            for theEngage in engagements:
                                for theBlue in lbluetooths:
                                    for theAsymp in asymptoms:
                                        tag = 'City_' + str(theCitySize) + '_strategy' + str(theStrategy) + '_probability' + prob + '_testing' + str(theTest) + '_engage' + str(theEngage) + '_lblue' + str(theBlue) + '_asymp' + str(theAsymp) + '_delay' + delay
                                        makeTag(runfile, tag, theCitySize, theStrategy, theTest, theEngage, theBlue, theAsymp, prob, options.nseed, options.nseedcity, delay)
        elif theStrategy == 4:
            for theCitySize in citySizes:
                for delay in delays:
                    for prob in probability:
                        for theEngage in engagements:
                            for theBlue in lbluetooths:
                                for theAsymp in asymptoms:
                                    tag = 'City_' + str(theCitySize) + '_strategy' + str(theStrategy) + '_probability' + prob + '_engage' + str(theEngage) + '_lblue' + str(theBlue) + '_asymp' + str(theAsymp)  + '_delay' + delay
                                    makeTag(runfile, tag, theCitySize, theStrategy, tests[0], theEngage, theBlue, theAsymp, prob, options.nseed, options.nseedcity, delay)
 
    runfile.close()
