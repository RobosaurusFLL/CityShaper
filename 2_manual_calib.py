#!/usr/bin/env micropython

import sys

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.button import Button
import os
os.system('setfont Lat15-TerminusBold32x16')

# Manually move the robot to calibrate light sensor
# in case that the other automatical one is not allowed during competetion

btn = Button()

cl = ColorSensor(INPUT_1)
cr = ColorSensor(INPUT_4)

r_white = cr.reflected_light_intensity
l_white = cl.reflected_light_intensity
print("Ready, move to black")
while btn.buttons_pressed == []:
    pass
r_black = cr.reflected_light_intensity
l_black = cl.reflected_light_intensity

print(l_black, file=sys.stderr)
print(l_white, file=sys.stderr)
print(r_black, file=sys.stderr)
print(r_white, file=sys.stderr)

o=open("data_calib.py", "w")
o.write("l_black = " + str(l_black) + "\n")
o.write("l_white = " + str(l_white) + "\n")
o.write("r_black = " + str(r_black) + "\n")
o.write("r_white = " + str(r_white) + "\n")
o.close()