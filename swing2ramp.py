#!/usr/bin/env micropython

import sys
import time

import os
import time
os.system('setfont Lat15-TerminusBold32x16')

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.motor import LargeMotor, MoveTank, MoveSteering

from line import Line_Flowering, square2line
from color import *
m = MoveSteering(OUTPUT_B, OUTPUT_C)
ml=LargeMotor(OUTPUT_B)
mr=LargeMotor(OUTPUT_C)



def rlidiff():
    return (left_color_sensor_rli() - right_color_sensor_rli()) + 50

def other_stoping_point():
    return(is_left_other_shade() and is_right_other_shade()) 

def stoping_point():
    return is_left_black() and is_right_black()

def base2line():
    m.on(0, -40)
    while right_color_sensor_rli() > 50:
        pass
    m.off()
    m.on_for_rotations(100, 20, 0.5)
    m.on(0, -40)
    while not is_right_white():
        pass
    while not is_right_black():
        pass
    while not is_right_white():
        pass
    m.off()

def go_2_end_of_line():
    #follow the line to the intersection
    Line_Flowering(right_color_sensor_rli, is_left_white, 2)
    Line_Flowering(right_color_sensor_rli, is_left_black, 2)
    Line_Flowering(right_color_sensor_rli, is_left_white, 2)
    Line_Flowering(right_color_sensor_rli, is_left_other_shade, 2, stop_at_end=True)
    mr.on(-20)
    while is_right_white() != True:
        pass
    #follow the line to the end by counting motor
    end_position = ml.position - (360 * 2.2)
    def on_for_rotations():
        return ml.position < end_position 
    
    Line_Flowering(right_color_sensor_rli, on_for_rotations, -2)

def endofline2stability():
    #turn to stability testing mission
    m.on_for_degrees(100, 20, (360 * 2))
    m.on_for_rotations(0, -30, 1.75)
    m.on_for_degrees(100, -20, (360 * 2))
    m.on_for_seconds(0, -20, 4)

  
def stability2elevator():
    m.on(0, 30)
    while not is_left_white():
        pass
    while not is_left_black():
        pass
    while not is_left_white():
        pass
    m.off()
    Line_Flowering(rlidiff, other_stoping_point, 2, stop_at_end=True)
#Turing around
    m.on_for_rotations(0, -10, 0.2)
    m.on(100, -30)
    while not is_right_white():
        pass
    while not is_right_black():
        pass
    while not is_right_white():
        pass
    m.off()
    Line_Flowering(rlidiff, stoping_point, 2, stop_at_end=True)
    m.on_for_rotations(0, -20, 0.5)
    m.on(100, -30)
    while not is_right_white():
        pass
    while not is_right_black():
        pass
    while not is_right_white():
        pass
    m.off()

def ramp_mission():
    Line_Flowering(rlidiff, stoping_point, 2, stop_at_end=True)
    #square2Otherline()
    m.on_for_rotations(0, -30, 4.2)
    m.on(0, -20)
    while left_color_sensor_rli() < 50:
        pass
    m.off()
    m.on_for_rotations(0, -10, 1)
    m.on_for_rotations(100, -10, 0.6)

def swing2ramp():
    base2line()
    go_2_end_of_line()
    endofline2stability()
    stability2elevator()
    ramp_mission()

if __name__ == "__main__":
    swing2ramp()