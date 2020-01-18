#!/usr/bin/env micropython

import sys
import time

from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_2
from color import *
from move import *
from line import *

ml = get_left_action_motor()
mr = get_right_action_motor()

def push2blackcircle_and_crane():
    #turnning onto the beginning of the circle-ish line
    drive_until(is_left_black, -30, -40)
    #crossing over to other end of circle-ish line
    drive_until(is_right_black, -30, -50)
    drive_until(is_right_white)
    drive_until(is_right_other_shade, stop_at_end=True)
    #utilizing the edge of the shaded part between two ends of circle-ish line

    Line_Flowering(right_color_sensor_rli, is_left_other_shade, 2, max_speed = -30,min_speed=-15)
    #drive_until(is_left_black, 70, -20)
    #following circle-ish line to push attachment into crane
    Line_Flowering(left_color_sensor_rli, is_right_black, 1.5, max_speed = -30, min_speed=-20)
    drive_until(is_right_black, 0, -10)
    drive_until(is_right_white, -15, -10)
    drive_for_seconds(-40, -20, 1)

def release_crane():
    mr.on_for_seconds(75, 0.5)
    time.sleep(1)
    mr.on_for_seconds(-75, 0.5)

def crane2home():
    drive_for_rotations(0, 20, 0.5)
    drive_for_rotations(0, 60, 2)
    ml.on_for_seconds(75, 0.5)
    drive_for_rotations(100, -100, 1.5)
    drive_for_seconds(0, 100, 2.5)
    drive_for_seconds(-100, -100, 1.5)

def blocks_and_crane():
    push2blackcircle_and_crane()
    release_crane()
    crane2home()

if __name__ == "__main__":
    blocks_and_crane()