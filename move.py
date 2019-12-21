#!/usr/bin/env micropython

import sys
import time

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.motor import LargeMotor, MoveTank, MoveSteering, MediumMotor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_2
from color import *
m=MoveSteering(OUTPUT_B, OUTPUT_C)
ml=LargeMotor(OUTPUT_B)
mr=LargeMotor(OUTPUT_C)
mmL=MediumMotor(OUTPUT_A)
mmR=MediumMotor(OUTPUT_D)

def get_left_action_motor():
    return mmL

def get_right_action_motor():
    return mmR

def drive_for_rotations(steering, power, rotations):
    m.on_for_rotations(steering, power, rotations)

def drive_for_seconds(steering, power, seconds):
    m.on_for_seconds(steering, power, seconds)

def get_left_drive_motor():
    return ml

def get_right_drive_motor():
    return mr

def drive_until(when2stop, steering=999, power=0, stop_at_end=False):
    if steering != 999:
        m.on(steering, power)

    while when2stop() != True:
        pass
    if stop_at_end:
        m.off()