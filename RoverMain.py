import numpy as np
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

    def loop(self):
        pass


if __name__ == "__main__":
    roverMain = roverMain()