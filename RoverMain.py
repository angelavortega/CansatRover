import time
import csv  
from data.roverData import roverData
from stages.launch import roverLaunch
from stages.land import roverLand
from stages.returnR import roverReturn


"""
This is the where all the magic happens
"""

class roverMain():
    
    def __init__(self):
        with open('data/data.csv', 'w') as f:
            writer = csv.writer(f)
            row = ['Time', 'Temperature', 'Pressure', 'Altitude', \
                    'X_Coordinate', 'Y_Coordinate', 'Roll', 'Pitch', 'Yaw']
            writer.writerow(row)     
        self.n = 0
        self.roverData = roverData()
        self.roverLaunch = roverLaunch(roverDataObj=self.roverData)
        self.roverLand = roverLand(roverDataObj=self.roverData)
        self.roverReturn = roverReturn(roverDataObj=self.roverData)

    def gatherData(self):
        # Initialize new list
        self.allData = [self.n]

        # Go to object class and gather all climate data and append to list 
        for value in self.roverData.climateData():
            self.allData.append(value)

        # Go to object class and gather all gps data and append       
        for value in self.roverData.gpsPosition():
            self.allData.append(value)

        # Go to object class aand gather acelorometer values and append
        for value in self.roverData.acelData():
            self.allData.append(value)
    
        self.n += 1

        return self.allData # list with data

    def saveData(self, datos):
        with open('data/data.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(datos)

    def sendMessage(self):
        return self.roverData.sendRadioData(self.allData)


if __name__ == "__main__":

    # Create new instance of our data gatherer
    roverMain = roverMain()


    while True:
        time.sleep(.25)
        datos = roverMain.gatherData()
        roverMain.saveData(datos)
        # Check if function sendMessage works 
        "Go to function sendMessage in roverData.py"
        roverMain.sendMessage()
        print(datos[1], 'is type', type(datos[1]))
