import time
import pandas as pd
from data.roverData import roverData
from stages.launch import roverLaunch
from stages.land import roverLand
from stages.returnR import roverReturn


class roverMain():
    
    def __init__(self):
        self.cities = pd.DataFrame(columns=['Time', "Temperature", "Pressure", "Humidity",  \
            "GPS", "ax", "ay", "az", "wx", "wy", "wz", "mx", "my", "mz"])
        self.cities.to_csv('data/data.csv', index=False)
        self.n = 0
        self.roverData = roverData()
        self.roverLaunch = roverLaunch(roverDataObj=self.roverData)
        self.roverLand = roverLand(roverDataObj=self.roverData)
        self.roverReturn = roverReturn(roverDataObj=self.roverData)

    def gatherData(self):
        self.allData = [self.n]
        self.n += 1
        for value in self.roverData.climateData():
            self.allData.append(value)
        self.allData.append(self.roverData.gpsPosition())
        for value in self.roverData.acelData():
            self.allData.append(value)
        return self.allData

    def saveData(self, datos):
        df = pd.DataFrame(datos).T
        df.to_csv('data/data.csv', mode='a', header=False, index=False)

    def sendMessage(self):
        return self.roverData.climateData(self.allData)


if __name__ == "__main__":
    roverMain = roverMain()
    while True:
        time.sleep(1)
        datos = roverMain.gatherData()
        roverMain.saveData(datos)
        print(datos)
