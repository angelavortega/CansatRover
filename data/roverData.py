import serial, time # For GPS
from data.sensors.lib_bme280 import * # Temperature, Humidity and Pressure
from data.sensors.lib_mpu9250 import * # Acelerometer
from data.sensors.RF_communication2 import * # Radio 


class roverData():
    
    def __init__(self):
        self.gpsSerial = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)
        
    def climateData(self):
        """
        (chip_id, chip_version) = readBME280ID()
        print ("Chip ID     :", chip_id)
        print ("Version     :", chip_version)
        """
        temperature, pressure, humidity = readBME280All()
        return [temperature, pressure, humidity]
    
    def gpsPosition (self):
        if(self.gpsSerial.in_waiting):
            position = self.gpsSerial.readline()
            self.lastPosition = position
            return position.decode()
        return self.lastPosition.decode()

    def acelData(self):
        flag = True
        while flag:
            try:
                ax,ay,az,wx,wy,wz = mpu6050_conv() # read and convert mpu6050 data
                mx,my,mz = AK8963_conv() # read and convert AK8963 magnetometer data
                flag = False
            except:
                continue
        return [ax, ay, az, wx, wy, wz, mx, my, mz]

    def sendRadioData(self, message):
        while len(message) < 32:
            message.append(0)
        radio.write(message) 
        return message

