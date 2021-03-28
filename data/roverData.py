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

        gpgga_info = '$GPGGA,'
        GPGGA_buffer = 0
        NMEA_buff = 0

        def convert_to_degrees(raw_value):
            decimal_value = raw_value/100.00
            degrees = int(decimal_value)
            mm_mmmm = (decimal_value – int(decimal_value))/0.6
            position = degrees + mm_mmmm
            return position        
        
        received_data = (str)(self.gpsSerial.readline()) #read NMEA string received
        GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                
        if (GPGGA_data_available>0):
            GPGGA_buffer = received_data.split('$GPGGA,',1)[1]  #store data coming after “$GPGGA,” string
            NMEA_buff = (GPGGA_buffer.split(','))
            nmea_latitude = []
            nmea_longitude = []
            nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
            nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
            lat = (float)(nmea_latitude)
            lat = convert_to_degrees(lat)
            longi = (float)(nmea_longitude)
            longi = convert_to_degrees(longi)
            self.lastPosition = [lat, longi]
            return [lat, longi]
        return self.lastPosition

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

