import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

GPIO.setmode(GPIO.BCM)

pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0,17)

radio.setPayloadSize(32)
radio.setChannel(0x77)
radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipes[0])
radio.printDetails()

iteracion = 0
   
while True:
    #message = list(input('Ingrese su mensaje'))
    iteracion = iteracion + 1
    message = list('Hello World {}'.format(iteracion))
    #while len(message) < 32:
    #    message.append(0)
    print(message) 
    radio.write(message)
    time.sleep(2)
    