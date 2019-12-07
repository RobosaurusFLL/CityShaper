#!/usr/bin/env micropython

import sys
import time

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.motor import LargeMotor, MoveTank, MoveSteering
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_2
from color import *
m=MoveSteering(OUTPUT_B, OUTPUT_C)
ml=LargeMotor(OUTPUT_B)
mr=LargeMotor(OUTPUT_C)

def push2redcircle():
    def on_for_rotations():
        return ml.position < end_position 
    end_position = ml.position - (360 * 6)

    #push blocks :'D
    m.on(0, -40)
    while on_for_rotations() != True:
        pass
    m.off()
    m.on_for_rotations(0, 20, 0.5)
    m.on_for_rotations(0, 100, 2)
    m.on_for_rotations(100, -20, 0.5)
    m.on_for_seconds(0, 100, 3)
    m.on_for_degrees(100, 30, 360 * 2.5)

def push2blackcircle():
    def on_for_rotations():
        return ml.position < end_position 

    end_position = ml.position - (360 * 3.5)

    #push blocks :'D
    m.on(0, -40)
    while on_for_rotations() != True:
        pass
    m.off()
    m.on_for_rotations(0, 100, 1.5)

    m.on_for_degrees( 100, -30, 360 * (90 / 45))
    m.on_for_seconds(0, 100, 1.5)
    m.on_for_degrees(100, 30, 360 * (90 / 45))

if __name__ == "__main__":
    push2redcircle()