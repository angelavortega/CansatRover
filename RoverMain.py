import time
from data.roverData import roverData
from stages.launch import roverLaunch
from stages.land import roverLand
from stages.returnR import roverReturn


class roverMain():
    
    def __init__(self):
        
        self.roverData = roverData()
        self.roverLaunch = roverLaunch(roverDataObj=self.roverData)
        self.roverLand = roverLand(roverDataObj=self.roverData)
        self.roverReturn = roverReturn(roverDataObj=self.roverData)

    def gatherData(self):
        self.allData = []
        self.allData.append(self.roverData.climateData())
        self.allData.append(self.roverData.gpsPosition())
        self.allData.append(self.roverData.acelData())
        return self.allData

    def sendMessage(self):
        return self.roverData.climateData(self.allData)

if __name__ == "__main__":
    roverMain = roverMain()
    while True:
        time.sleep(1)
        print(roverMain.gatherData())