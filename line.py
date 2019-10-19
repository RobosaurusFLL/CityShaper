#!/usr/bin/env micropython

import sys
import time

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.motor import LargeMotor, MoveTank, MoveSteering
from color import *
m=MoveSteering(OUTPUT_B, OUTPUT_C)

   
def Line_Flowering(normalize_rli, when2stop, gain, max_speed=-40, min_speed=-5, stop_at_end=False):
    while not when2stop():
        r = normalize_rli() 
        diff = (r - 50) * gain  #calculating difference

        #limiting difference
        if diff > 100:
            diff = 100
        if diff < -100:
            diff = -100
        sp = max_speed * (1 - abs(diff)/100) + min_speed  #go faster when diff is smaller
        #making sure speed is not larger than intended
        if abs(sp) > abs(max_speed):
            sp = max_speed
        m.on(diff, sp) #running
    if stop_at_end == True:
        m.off()



def square2line():
    for i in range (3):
        while left_color_sensor_rli() < 50:
            m.on(50, -5) 
        while left_color_sensor_rli() > 50:
            m.on(50, 5)
        while right_color_sensor_rli() < 50:
            m.on(-50, -5)
        while right_color_sensor_rli() > 50:
            m.on(-50, 5)
    m.off()
    




