#!/usr/bin/env micropython

import sys
import time

from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_2
from color import *
from move import *

ml = get_left_drive_motor()

def push2redcircle():
    def on_for_rotations():
        return ml.position < end_position 
    end_position = ml.position - (360 * 6)

    #push blocks :'D
    drive_until(on_for_rotations, 0, -40, True)

    drive_for_rotations(0, 20, 0.5)
    drive_for_rotations(0, 100, 2)
    drive_for_rotations(100, -50, 0.5)
    drive_for_seconds(0, 100, 3)
    drive_for_rotations(100, 50, 2.5)

def push2blackcircle():
    def on_for_rotations():
        return ml.position < end_position 

    end_position = ml.position - (360 * 3.5)

    #push blocks :'D
    drive_until(on_for_rotations, 0, -40, True)
    drive_for_rotations(0, 100, 1.5)

    drive_for_rotations( 100, -50, 2)
    drive_for_seconds(0, 100, 1.5)
    drive_for_rotations(100, 50, 3)

if __name__ == "__main__":
    push2blackcircle()