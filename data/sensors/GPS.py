import serial, time


gpsSerial = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)

while True:
    if(gpsSerial.in_waiting):
        position =gpsSerial.readline()
        print (position.decode())
        time.sleep(0.2)
