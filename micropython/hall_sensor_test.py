# Python script used to determine the magnet polarity that triggers the hall effect sensor

from machine import Pin, Timer
from time import sleep

# Initialize GPIO14 pin as input
sensor = Pin(1, Pin.IN, Pin.PULL_DOWN)

# Continuous loop for continuous serial output
while True:
    if sensor.value() == 0:
        print("No magnetic field")
    else:
        print("Magnetic field")
    print("---------------------------------------")
    sleep(0.5)
