from CitySimulator.City import City




if __name__ == "__main__":

    city = City(1000, 40, 10, 50000, 0.5, 0.3, 0.2, 3, 16)
    for i in range(0, 24*60):
        city.run(i)
        print('Time is: ' + str(i))
        city.thePopulation[0].Print()



 

