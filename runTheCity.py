from CitySimulator.City import City




if __name__ == "__main__":

    city = City('/home/pablom/Documentos/BlueHook/CityConf.cfg')
    #city.Print(2)
    for i in range(0, 24*60):
        city.run(i)
        print('Time is: ' + str(i))
        city.thePopulation[0].Print()



 

