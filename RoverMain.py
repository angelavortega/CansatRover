import time
import csv  
from data.roverData import roverData
from stages.launch import roverLaunch
from stages.land import roverLand
from stages.returnR import roverReturn


class roverMain():
    
    def __init__(self):
        with open('data/data.csv', 'w') as f:
            writer = csv.writer(f)
            row = ['Time', 'Temperature', 'Pressure', 'Altitude', 'Humidity', \
                    'X_Cordinate', 'Y_Cordinate', 'ax', 'ay', 'az', 'wx', 'wy',\
                    'wz', 'mx', 'my', 'mz']
            writer.writerow(row)     
        self.n = 0
        self.roverData = roverData()
        self.roverLaunch = roverLaunch(roverDataObj=self.roverData)
        self.roverLand = roverLand(roverDataObj=self.roverData)
        self.roverReturn = roverReturn(roverDataObj=self.roverData)

    def gatherData(self):
        self.allData = [self.n]
        for value in self.roverData.climateData():
            self.allData.append(value)
        for value in self.roverData.gpsPosition():
            self.allData.append(value)
        for value in self.roverData.acelData():
            self.allData.append(value)
        self.n += 1
        return self.allData

    def saveData(self, datos):
        with open('data/data.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(datos)

    def sendMessage(self):
        return self.roverData.sendRadioData(self.allData)


if __name__ == "__main__":
    roverMain = roverMain()
    while True:
        time.sleep(1)
        datos = roverMain.gatherData()
        roverMain.saveData(datos)
        print(datos)
