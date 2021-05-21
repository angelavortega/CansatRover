import time
import csv  
import json
from data.roverData import roverData # Class in charge of reading sensor data (for more details go to the folder data and open roverData.py)
from stages.launch import roverLaunch # Class in charge of launch phase
from stages.land import roverLand
from stages.returnR import roverReturn


# Creation of class roverMain which is going to have complet control over all stages
class roverMain():
    
    def __init__(self):
        json_path = 'data/csv_num.json'
        with open(json_path, 'r') as f:
            csv_num = json.load(f)
        self.csv_path = 'data/tests/data_{}.csv'.format(csv_num['number']) 
        csv_num['number'] = csv_num['number'] + 1
        with open(json_path, 'w') as f:
            json.dump(csv_num, f, indent=1)
        with open(self.csv_path, 'w') as f:
            writer = csv.writer(f)
            row = ['Index', 'Time', 'Temperature', 'Pressure', 'Altitude', \
                    'X_Coordinate', 'Y_Coordinate', 'Roll', 'Pitch', 'Yaw']
            writer.writerow(row)     
        self.n = 0
        self.roverData = roverData()
        self.Launch = roverLaunch()
        self.Land = roverLand()
        self.Return = roverReturn()
        self.initial_pos = True
        in_posx = []
        in_posy = []
        for val in range(0, 13):
            x, y = self.roverData.gpsPosition()
            in_posx.append(x)
            in_posy.append(y)
        in_posx = sum(in_posx) / len(in_posx)
        in_posy = sum(in_posy) / len(in_posy)
        self.gps_pos(in_posx, in_posy)
        self.last_time = time.time()

    def gps_pos(self, x_lat, y_lat):
        if self.initial_pos: 
            self.in_x = x_lat
            self.in_y = y_lat
            self.initial_pos = False 
            return [0, 0]
        x = x_lat - self.in_x
        y = y_lat - self.in_y
        return [x, y]
        
    def gatherData(self):
        allData = [self.n]
        actl_time = time.time() - self.last_time
        allData.append(actl_time)
        self.last_time = actl_time
        for value in self.roverData.climateData():
            allData.append(value)
        x, y = self.roverData.gpsPosition()
        for value in self.gps_pos(x, y):
            allData.append(value)
        for value in self.roverData.acelData():
            allData.append(value)
        self.n += 1
        return allData

    def saveData(self, data):
        with open(self.csv_path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(data)

    def sendMessage(self, data):
        return self.roverData.sendRadioData(data)
    
    def controlStage(self, data, stage):
        if stage == 0:
            self.Launch.checkParashut(data)
        if stage == 1:
            self.Land.casatController(data)
        if stage == 2:
            self.Return.roverController(data)


if __name__ == "__main__":
    roverMain = roverMain()
    time_frequecy = .25

    while True:
        time.sleep(time_frequecy)
        data = roverMain.gatherData()
        roverMain.saveData(data)
        roverMain.sendMessage(data)
        stage = 1
        roverMain.controlStage(data, stage)
        print(data)
