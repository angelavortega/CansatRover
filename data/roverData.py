import serial, time # For GPS
import math
from data.sensors.bmp388 import * # Temperature, Altitude and Pressure
from data.sensors.berryIMU import * # Acelerometer, Gyroscope and magnetometer
from data.sensors.RF_communication2 import * # Radio 


class roverData():
    
    def __init__(self):
        self.gpsSerial = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)
        self.bmp388 = BMP388()
        self.initial = True
        
    def climateData(self):
        """
        (chip_id, chip_version) = readBME280ID()
        print ("Chip ID     :", chip_id)
        print ("Version     :", chip_version)
        """
        temperature, pressure, altitude = self.bmp388.get_temperature_and_pressure_and_altitude()
        altitude = self.calcAltitude(altitude)
        return [temperature, pressure, altitude]
    """
    def calcAltitude(self, pressure):
        if self.initial: 
            self.intlPressure = pressure
            self.initial = False 
            return 0
        else:
            altitude = (self.intlPressure - pressure) / (self.airDensity * self.gravity)
            return round(altitude, 1)
    """
    def calcAltitude(self, altitude):
        if self.initial: 
            self.intlAltitude = altitude
            self.initial = False 
            return 0
        else:
            altitude = altitude - self.intlAltitude
            return round(altitude, 1)

    def gpsPosition(self):

        gpgga_info = '$GPGGA,'
        GPGGA_buffer = 0
        NMEA_buff = 0

        def convert_to_degrees(raw_value):
            decimal_value = raw_value / 100.00
            degrees = int(decimal_value)
            mm_mmmm = (decimal_value - int(decimal_value)) / 0.6
            position = degrees + mm_mmmm
            return position        
        
        def convert_to_m(latitude, longitude):
            y = latitude * 111319.4
            x = longitud * math.cos(math.radians(longitude)) * 111319.4
            return x, y

        while True:
            try:
                received_data = (str)(self.gpsSerial.readline()) #read NMEA string received
                GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                
                if (GPGGA_data_available > 0):
                    GPGGA_buffer = received_data.split('$GPGGA,', 1)[1]  #store data coming after “$GPGGA,” string
                    NMEA_buff = (GPGGA_buffer.split(','))
                    nmea_latitude = []
                    nmea_longitude = []
                    nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
                    nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
                    lat = (float)(nmea_latitude)
                    lat = convert_to_degrees(lat)
                    longi = (float)(nmea_longitude)
                    longi = convert_to_degrees(longi)
                    x, y = convert_to_m(lat, longi)
                    return [x, y]
            except:
                continue

    def acelData(self):
        flag = True
        while flag:
            try:
                roll, pitch, yaw = accMagGyData()
                flag = False
            except:
                continue
        return [roll, pitch, yaw]

    def sendRadioData(self, message):
        while len(message) < 32:
            message.append(0)
        radio.write(message) 
        return message

