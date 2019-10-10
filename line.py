#!/usr/bin/env micropython

import sys
import time

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.motor import LargeMotor, MoveTank, MoveSteering
from color import *
m=MoveSteering(OUTPUT_B, OUTPUT_C)

offset = -15    
def Line_Flowering(normalize_rli, when2stop, gain, max_speed):
    while not when2stop():
        r = normalize_rli() 
        diff = (r - 50) * gain  #calculating difference

        #limiting difference
        if diff > 100:
            diff = 100
        if diff < -100:
            diff = -100
        sp = max_speed * (1 - abs(diff)/100) + offset  #go faster when diff is smaller
        #making sure speed is not larger than intended
        if abs(sp) > abs(max_speed):
            sp = max_speed
        m.on(diff, sp) #running



def square2line():
    for i in range (3):
        while left_color_sensor_rli() < 50:
            m.on(50, -5) 
        while left_color_sensor_rli() > 50:
            m.on(50, 5)
        while right_color_sensor_rli() < 50:
            m.on(-50, -5)
        while right_color_sensor_rli() > 50:
            #print(right_color_sensor_rli(), file=sys.stderr)
            m.on(-50, 5)
    m.off()
    




