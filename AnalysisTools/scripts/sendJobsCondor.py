from optparse import OptionParser
import os
import stat

##########################################################################################
theExecutable = """#!/bin/bash
cd /afs/cern.ch/work/p/pablom/private/Tracking/CMSSW_11_1_0_pre5/src
eval `scramv1 runtime -sh`
cd /afs/cern.ch/work/p/pablom/private/BlueHook/
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
incubationLambda 4
#Bluetooth radius in meters
bluetoothRadius BLUETOOTHRADIUS
#Infection radius in meters
infectionRadius 2
#Infection probability given as probability of infecting someone being together 30 minutes
infectionProbability 0.1
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

"""
###########################################################################################

###########################################################################################
Condor = """#!/bin/bash

universe                = vanilla
executable              = $(filename)
output                  = LOGDIR/$(ClusterId).$(ProcId).out
error                   = LOGDIR/$(ClusterId).$(ProcId).err
log                     = LOGDIR/$(ClusterId).log
Notify_user             = pablom@cern.ch
+JobFlavour = "tomorrow" 
queue filename matching (CitySize*/run_*sh)

"""
###########################################################################################


def makeTag(thefile, tag, citysize, strategy, test, engagement, lbluetooth, asympton, nseed, nseedcity):


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


    (options, args) = parser.parse_args()

    citySizes = options.citysize.split(',')
    strategies = options.strategy.split(',')
    tests = options.tests.split(',')
    engagements = options.engagement.split(',')
    lbluetooths = options.lbluetooth.split(',')
    asymptoms = options.asymptoms.split(',')

    runfile = open('toRun.tcl', 'w')
    logs = os.getcwd() + '/logs'
    os.mkdir(logs)
    theCondor = Condor
    theCondor = theCondor.replace("LOGDIR", logs)
    runfile.write(theCondor)
    runfile.close()



    for theStrategyk in strategies:
        theStrategy = int(theStrategyk)
        if theStrategy == 0:
            for theCitySize in citySizes:
                tag = 'City_' + str(theCitySize) + '_strategy0' 
                makeTag(runfile, tag, theCitySize, theStrategy, tests[0], engagements[0], lbluetooths[0], asymptoms[0], options.nseed, options.nseedcity)
        elif theStrategy == 1 or theStrategy == 2:
            for theCitySize in citySizes:
                for theTest in tests:
                    tag = 'City_' + str(theCitySize) + '_strategy' + str(theStrategy) + '_testing' + str(theTest)
                    makeTag(runfile, tag, theCitySize, theStrategy, theTest, engagements[0], lbluetooths[0], asymptoms[0], options.nseed, options.nseedcity)
        elif theStrategy == 3 or theStrategy == 5:
            for theCitySize in citySizes:
                for theTest in tests:
                    for theEngage in engagements:
                        for theBlue in lbluetooths:
                            for theAsymp in asymptoms:
                                tag = 'City_' + str(theCitySize) + '_strategy' + str(theStrategy) + '_testing' + str(theTest) + '_engage' + str(theEngage) + '_lblue' + str(theBlue) + '_asymp' + str(theAsymp)
                                makeTag(runfile, tag, theCitySize, theStrategy, theTest, theEngage, theBlue, theAsymp, options.nseed, options.nseedcity)
        elif theStrategy == 4:
            for theCitySize in citySizes:
                for theEngage in engagements:
                    for theBlue in lbluetooths:
                        for theAsymp in asymptoms:
                            tag = 'City_' + str(theCitySize) + '_strategy' + str(theStrategy) + '_engage' + str(theEngage) + '_lblue' + str(theBlue) + '_asymp' + str(theAsymp)
                            makeTag(runfile, tag, theCitySize, theStrategy, tests[0], theEngage, theBlue, theAsymp, options.nseed, options.nseedcity)
 
