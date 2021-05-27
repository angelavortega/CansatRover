import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)


class roverLand():
    
    def __init__(self):
        self.servo1 = GPIO.PWM(18, 50)
        self.servo2 = GPIO.PWM(22, 50)
        self.servo1.start(2.5)
        self.servo2.start(2.5)
        self.last_Temperature = 0 
        self.last_Pressure = 0
        self.last_Altitude = 0
        self.last_X_Coordinate = 0
        self.last_Y_Coordinate = 0
        self.last_Roll = 0
        self.last_Pitch = 0
        self.last_Yaw = 0
        self.servoControl(2, 12)
        time.sleep(.5)
        self.servoControl(12, 2)
        time.sleep(.5)
        self.servoControl(7, 7)

    def checkLanding(self):
        "This function checks if the landing is done"
        pass

    def servoControl(self, duty_Cycle_1, duty_Cycle_2):
        "This function controls the movement of the servo"
        # Un 12 en el duty cycle equivale a 180° en el servo
        # Y un 2 a un 0°

        self.servo1.ChangeDutyCycle(float(duty_Cycle_1))
        # TODO avoid the time sleep and do it simultainiously with all the code
        time.sleep(.5)
        self.servo2.ChangeDutyCycle(float(duty_Cycle_2))
    
    def casatController(self, data):
        Index, Time, Temperature, Pressure, Altitude, X_Coordinate, Y_Coordinate, Roll, Pitch, Yaw = data

        #### Here goes control algorithm ####

        """Example of how to use self.last_values
        fall_velocity = (Altitud - self.last_Altitude) / Time
        x_velocity = (X_Coordinate - self.last_X_Coordinate) / Time
        """
        
        duty_1 = 12
        duty_2 = 12
        #####################################

        self.last_Altitude = Altitude
        self.last_X_Coordinate = X_Coordinate
        self.last_Y_Coordinate = Y_Coordinate
        self.last_Roll = Roll
        self.last_Pitch = Pitch
        self.last_Yaw = Yaw
        self.servoControl(duty_1, duty_2)
