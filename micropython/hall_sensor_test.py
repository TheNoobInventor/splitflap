# Hall sensor test to determine how to place the magnet to trigger the sensor

from machine import Pin, Timer
from time import sleep
# Initialization of GPIO14 as input
sensor = Pin(1, Pin.IN, Pin.PULL_DOWN)
# Continuous loop for continuous serial output
while True:
    if sensor.value() == 0:
        print("No magnetic field")
    else:
        print("Magnetic field")
    print("---------------------------------------")
    sleep(0.5)
