import time
import csv  
import os
import json
from data.roverData import roverData # Class in charge of reading sensor data (for more details go to the folder data and open roverData.py)
from stages.launch import roverLaunch # Class in charge of launch phase
from stages.land import roverLand
from stages.returnR import roverReturn

time_frequecy = .25 # The time at which the program will be running in seconds


# Creation of class roverMain which is going to have complet control over all stages
class roverMain():
    
    def __init__(self):
        self.roverData = roverData()
        self.Launch = roverLaunch()
        self.Land = roverLand()
        self.Return = roverReturn()
        self.set_csv()
        self.set_gps()
        self.n = 0
        self.last_time = time.time()

    def set_csv(self):
        ### This function creates the CSV were all data is going to be stored
        tests_path = 'data/tests'
        if not os.path.exists(tests_path): os.mkdir(tests_path) # Creates the tests folder if it doesn't exist
        number = len(os.listdir(tests_path)) # Checks the lenght of the tests folder and saves the number
        self.csv_path = 'data/tests/data_{}.csv'.format(number) # Creates CSV file with the number as legth
        with open(self.csv_path, 'w') as f:
            writer = csv.writer(f)
            row = ['Index', 'Time(s)', 'Temperature(C)', 'Pressure(Pa)', 'Altitude(m)', \
                    'X_Coordinate(m)', 'Y_Coordinate(m)', 'Roll(radians)', 'Pitch(radians)', 'Yaw(deg)']
            writer.writerow(row)     
    
    def set_gps(self):
        ### Set the origin position in the GPS
        self.initial_pos = True # Made to stablish initial GPS coordinates
        in_posx = []
        in_posy = []
        for val in range(0, 13):
            # Read 13 times the GPS data
            x, y = self.roverData.gpsPosition()
            in_posx.append(x)
            in_posy.append(y)
        in_posx = sum(in_posx) / len(in_posx) # Average of x position
        in_posy = sum(in_posy) / len(in_posy) # Average of y position
        self.gps_pos(in_posx, in_posy) # Send averages as initial conditions in x and y

    def gps_pos(self, x_lat, y_lat):
        ### Returns how far from origin are x and y corrdinates in meters 
        if self.initial_pos: 
            # Save initial position in x and y
            self.in_x = x_lat
            self.in_y = y_lat
            self.initial_pos = False 
            return [0, 0]
        x = x_lat - self.in_x # x and y minus the initialcoordinate
        y = y_lat - self.in_y
        return [x, y]
        
    def gatherData(self):
        ### Gathers data from all electronic components
        allData = [self.n] # Index value
        actl_time = time.time() - self.last_time
        allData.append(actl_time) # Time it took since last time
        self.last_time = time.time() 
        for value in self.roverData.climateData():
            # [temperature, pressure, altitude]
            allData.append(value)
        x, y = self.roverData.gpsPosition() # Raw values from gps
        for value in self.gps_pos(x, y): # substracted initial coordinates from x and y
            # [x, y]
            allData.append(value)
        for value in self.roverData.acelData():
            # [roll, pitch, yaw]
            allData.append(value)
        self.n += 1 # Increment index value by 1
        return allData

    def saveData(self, data):
        ### Saves new line of data in the csv
        with open(self.csv_path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(data)

    def sendMessage(self, data):
        ### Sends data to ground interface
        return self.roverData.sendRadioData(data)
    
    def controlStage(self, data, stage):
        ### Controls the stage to which the data is going to be sent
        if stage == 0:
            self.Launch.checkParashut(data)
        if stage == 1:
            self.Land.casatController(data)
        if stage == 2:
            self.Return.roverController(data)


if __name__ == "__main__":
    roverMain = roverMain()# create object roverMain

    while True:
        #time.sleep(time_frequecy)
        data = roverMain.gatherData() # Gather the data
        # TODO add section that determines in which stage we are located
        stage = 1 # Stage one is by default here
        roverMain.controlStage(data, stage) # Send data to the specific stage
        roverMain.saveData(data) # Save the data
        roverMain.sendMessage(data) # Send data by radio to the interface
        print(data)
