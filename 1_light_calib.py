#!/usr/bin/env micropython

import sys

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.motor import LargeMotor, MediumMotor, MoveTank, MoveSteering
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor

m = MoveSteering(OUTPUT_B, OUTPUT_C)
cl = ColorSensor(INPUT_1)
cr = ColorSensor(INPUT_4)
#setting reflective light intensities (rli) to unrealistic values to make sure they're replaced
l_black = 100
l_white = 0
r_black = 100
r_white = 0
m.left_motor.position = 0
m.on(0, 20)
#driving (over a line) and collecting the brightest and darkest rlis
while m.left_motor.position < 360:
    rli = cl.reflected_light_intensity
    if l_black > rli:
        l_black = rli
    if l_white < rli:
        l_white = rli
    rli = cr.reflected_light_intensity
    if r_black > rli:
        r_black = rli
    if r_white < rli:
        r_white = rli
m.off()

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