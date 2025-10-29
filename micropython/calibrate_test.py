from machine import Pin

from Calibrate import calibrate, calculate_offsets
from Panel import Panel
from ElementGpio import ElementGpio

panel = Panel([
    #ElementGpio(2, 28, 27, 26, 22, reverse_direction=True), # Motor A with sensor B
    ElementGpio(14, 18, 19, 20, 21, reverse_direction=True), # Motor B with sensor A
])

step = calibrate(panel, num_elements=1)

step(1479) # this eventually calls the respective step() function depending on if it's ElementGPIO or ElementUart

calculate_offsets()