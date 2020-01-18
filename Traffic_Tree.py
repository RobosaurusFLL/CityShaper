#!/usr/bin/env micropython

import sys
import time

from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_2, INPUT_3
from line import Line_Flowering, square2line, square2Otherline
from color import *
from move import *
ml=get_left_drive_motor()
mr=get_right_drive_motor()
mmL=get_left_action_motor()
us = UltrasonicSensor(INPUT_3)

def traffic2circle_ish_line():
    #going backwards to bump into traffic mission; following the south wall
    drive_for_rotations(-5, 50, 2.5)
    drive_for_seconds(-5, 20, 2.5)
    # go back
    drive_until(is_right_white, -5, -20, True)
    #Turning towards crane mission
    #Stoping at line connected to base
    drive_until(is_right_black, 32, -40, True)

def line2tree():
#following circle-ish line to tree
    drive_for_rotations(0, -30, 0.15)
    drive_until(is_right_black, 100, -40)
    drive_until(is_right_white, stop_at_end=True)

    def rlidiff():
        return (left_color_sensor_rli() - right_color_sensor_rli()) + 50

    def aimattree():
        return us.distance_centimeters < 14
    #following line until ultrasonic sensor reading decreases so that we know we're close to the tree
    Line_Flowering(rlidiff, aimattree, 1.5, min_speed=-30)
    def stoping_point():
        #using ultrasonic sensor
        return us.distance_centimeters > 25
    #stopping when the reading is larger afterwards because the right angle is just a little past the tree
    Line_Flowering(rlidiff, stoping_point, 1.5, max_speed = -20, stop_at_end=True)

    #end_position = mr.position - (360 * 1.1)
    #Line_Flowering(rlidiff, on_for_rotations, 1, max_speed=-30, stop_at_end=True)
    #activating attachment to push blocks onto tree
    mmL.on_for_seconds(-75, 0.5)
    time.sleep(1)

def tree2home():
    def close2wall():
        return us.distance_centimeters < 20
    drive_for_rotations(0, 100, 2.5)
    mmL.on(50)
    drive_for_rotations(100, 60, 1.4)
    mmL.off()
    drive_until(close2wall, 0, -100)
    drive_for_seconds(100, 75, 1)

def Traffic_Tree():
    traffic2circle_ish_line()
    line2tree()
    tree2home()

if __name__ == "__main__":
    Traffic_Tree()