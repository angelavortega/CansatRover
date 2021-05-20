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
        pass

    def checkLanding(self):
        "This function checks if the landing is done"
        pass

    def servoControl(self, duty_Cycle_1, duty_Cycle_2):
        "This function controls the movement of the servo"
        # Un 12 en el duty cycle equivale a 180° en el servo
        # Y un 2 a un 0°

        self.servo1.ChangeDutyCycle(float(duty_Cycle_1))
        self.servo2.ChangeDutyCycle(float(duty_Cycle_2))
    
    def casatController(self, data):
        Index, Time, Temperature, Pressure, Altitude, X_Coordinate, Y_Coordinate, Roll, Pitch, Yaw = data
        #### Here goes control algorithm ####
        
        #####################################
        duty_1 = 12
        duty_2 = 12
        
        self.servoControl(duty_1, duty_2)
