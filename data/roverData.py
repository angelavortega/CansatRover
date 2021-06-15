import serial
import time # For GPS
import math
from data.sensors.bmp388 import * # Temperature, Altitude and Pressure
from data.sensors.berryIMU import * # Acelerometer, Gyroscope and magnetometer
from data.sensors.RF_communication2 import * # Radio 


class roverData():
    
    def __init__(self):
        self.gpsSerial = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)
        self.bmp388 = BMP388()
        self.airDensity = 1.2041 # kg/m^3
        self.gravity = 9.81 # m/s^2
        self.initial = True
        
    def climateData(self):
        ### Returns  temperature, pressure and altitude
        """
        (chip_id, chip_version) = readBME280ID()
        print ("Chip ID     :", chip_id)
        print ("Version     :", chip_version)
        """
        temperature, pressure, altitude = self.bmp388.get_temperature_and_pressure_and_altitude()
        pressure = pressure / 100
        altitude = self.calcAltitude(pressure) # Calculates altitude
        return [temperature / 100, pressure, altitude]
    
    def calcAltitude(self, pressure):
        ### Returns altitude in meters
        if self.initial: 
            # Saves initial pressure
            self.intlPressure = pressure
            self.initial = False 
            return 0
        else:
            # Claculates actual altitude
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
    """

    def gpsPosition(self):
        ### Reads raw data from gps and transform data in latitude and longitude

        def convert_to_degrees(raw_value):
            # Converts raw value of GPS to degrees
            decimal_value = raw_value / 100.00
            degrees = int(decimal_value)
            mm_mmmm = (decimal_value - int(decimal_value)) / 0.6
            position = degrees + mm_mmmm
            return position        
        
        def convert_to_m(latitude, longitude):
            # Converts latitude and longitude to meters
            y = latitude * 111111.11
            x = longitude * math.cos(math.radians(latitude)) * 111111.11
            return x, y

        while True:
            try:
                received_data = (str)(self.gpsSerial.readline()) #read NMEA string received
                GPGGA_data_available = received_data.find('$GNGGA,')   #check for NMEA GPGGA string                
                if (GPGGA_data_available > 0):
                    GPGGA_buffer = received_data.split('$GNGGA,', 1)[1]  #store data coming after “$GPGGA,” string
                    NMEA_buff = (GPGGA_buffer.split(','))
                    nmea_latitude = []
                    nmea_longitude = []
                    nmea_latitude = NMEA_buff[1]       #extract latitude from GPGGA string
                    nmea_longitude = NMEA_buff[3]      #extract longitude from GPGGA string
                    lat = (float)(nmea_latitude)  
                    lat = convert_to_degrees(lat)
                    longi = (float)(nmea_longitude)
                    longi = convert_to_degrees(longi)
                    x, y = convert_to_m(lat, longi)
                    return [x, y]
            except:
                continue

    def acelData(self):
        ### Data from acelerometer, gyroscope and magnetometer in roll, pitch and yaw
        roll, pitch, yaw = accMagGyData()
        return [roll, pitch, yaw]

    def sendRadioData(self, data):
        ### Send data to the interface
        Y, Z, A, B, C, D, E, F, G, H = data
        data = [str(A), str(B / 100), str(C), str(D), str(E),\
            str(F), str(G), str(H)]
        # data = [Temperature(C), Pressure(hPA), Altitude(m), X(m), Y(m), Roll(rad), Pitch(deg), Yaw(deg)]
        data_id = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        i = 0
        for val in data:
            data_send = [data_id[i]]
            for l in val:
                data_send.append(l)      
            while len(data_send) < 32:
                data_send.append(0)
            radio.write(data_send)
            i += 1
    
    def rcvRadioData(self):
        ackPL = [1]
        while not radio.available(0):
            time.sleep(1 / 100)

        receivedMessage = []
        receivedMessage = radio.read(receivedMessage, radio.getDynamicPayloadSize())
        print("Received: {}".format(receivedMessage))

        print("Translating the receivedMessage into unicode characters...")
        string = ""
        for n in receivedMessage:
            # Decode into standard unicode set
            if (n >= 32 and n <= 126):
                string += chr(n)
        # print(string)
        return string
        #radio.writeAckPayload(1, ackPL, len(ackPL))
        #print("Loaded payload reply of {}".format(ackPL))    



