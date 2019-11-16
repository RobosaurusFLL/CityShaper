#!/usr/bin/env micropython

import sys
import time

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.motor import LargeMotor, MoveTank, MoveSteering
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_2
from line import Line_Flowering, square2line
from color import *
m=MoveSteering(OUTPUT_B, OUTPUT_C)
ml=LargeMotor(OUTPUT_B)
mr=LargeMotor(OUTPUT_C)

def traffic_crane_mission():
    #going backwards to bump into traffic mission; following the south wall
    m.on_for_rotations(-5, 50, 2.5)
    m.on_for_seconds(-5, 20, 2.5)
    # go back
    m.on(-5, -20)
    while is_right_white() != True:
        pass
    m.off()
    #Turning towards crane mission
    m.on(30, -30)
    #Stoping at line connected to base
    while is_left_black() != True:
        pass
    m.off()
    m.on(0, -20)
    while is_left_white() != True:
        pass
    m.off()
    #Finding dark blue area outside white circle
    m.on(0, -20)
    while left_color_sensor_rli() > 50:
        pass
    m.off()
    #Following edge of white circle
    Line_Flowering(left_color_sensor_rli, is_right_white, 2)
    #Pushing attachment into crane
    m.on_for_seconds(0, -5, 3)

if __name__ == "__main__":
    traffic_crane_mission()