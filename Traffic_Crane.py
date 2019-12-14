#!/usr/bin/env micropython

import sys
import time

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.motor import LargeMotor, MoveTank, MoveSteering, MediumMotor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_2
from line import Line_Flowering, square2line, square2Otherline
from color import *
m=MoveSteering(OUTPUT_B, OUTPUT_C)
ml=LargeMotor(OUTPUT_B)
mr=LargeMotor(OUTPUT_C)
mmL=MediumMotor(OUTPUT_A)

def traffic2circle_ish_line():
    #going backwards to bump into traffic mission; following the south wall
    m.on_for_rotations(-5, 50, 2.5)
    m.on_for_seconds(-5, 20, 2.5)
    # go back
    m.on(-5, -20)
    while is_right_white() != True:
        pass
    m.off()
    #Turning towards crane mission
    m.on(32, -40)
    #Stoping at line connected to base
    while is_right_black() != True:
        pass
    m.off()

def line2tree():
#following circle-ish line to tree
    m.on_for_rotations(0, -30, 0.15)
    m.on(100, -40)
    while not is_right_black():
        pass
    while not is_right_white():
        pass
    m.off()

    def rlidiff():
        return (left_color_sensor_rli() - right_color_sensor_rli()) + 50

    mr.position = 0
    ml.position = 0
    end_position = ml.position - (360 * 4)
    def on_for_rotations():
        return mr.position < end_position
#using difference of motors to see how much the robot has turned on the circle-ish line
    def stoping_point():
        #print(mr.position - ml.position, file=sys.stderr)
        if abs(ml.position) > abs(mr.position):
            mr.position = 0
            ml.position = 0
        return mr.position - ml.position < -700
    Line_Flowering(rlidiff, stoping_point, 1.5, min_speed=-30)

    end_position = mr.position - (360 * 1.1)
    Line_Flowering(rlidiff, on_for_rotations, 1, max_speed=-30, stop_at_end=True)
#activating attachment to push blocks onto tree
    mmL.on_for_seconds(-75, 2)
    time.sleep(1)

def tree2crane():
    m.on(-100, -40)
    while not is_left_white():
        pass
    while not is_left_other_shade():
        pass
    while not is_left_white():
        pass
    while not is_left_black():
        pass
    Line_Flowering(right_color_sensor_rli, is_left_white, 1.5, min_speed=-15)
    Line_Flowering(right_color_sensor_rli, is_left_black, 1.5, min_speed=-15)
    m.on(100, -20)
    while not is_right_other_shade():
        pass
    Line_Flowering(left_color_sensor_rli, is_right_white, -1.5, min_speed=-20)
    m.on(0, -30)
    while not is_right_black():
        pass
    while not is_right_white():
        pass
    m.off()
    m.on_for_seconds(0, -10, 1.5)

def crane2home():
    m.on_for_rotations(0, 60, 0.5)
    m.on_for_rotations(0, 100, 1)
    m.on_for_rotations(100, -30, 1.5)
    m.on_for_seconds(0, 100, 2.5)
    m.on_for_seconds(-100, -50, 1)
    #while not is_right_black():
    #    pass

def Traffic_Crane():
    traffic2circle_ish_line()
    line2tree()
    tree2crane()
    crane2home()


if __name__ == "__main__":
    Traffic_Crane()