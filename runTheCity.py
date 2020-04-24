from CitySimulator.City import City




if __name__ == "__main__":

    city = City('/home/pablom/Documentos/BlueHook/CityConf.cfg', 'ws://localhost:8182/gremlin')
    city.runDays(20)



 

