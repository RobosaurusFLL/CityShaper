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
    m.on(33, -40)
    #Stoping at line connected to base
    while is_left_black() != True:
        pass
    m.off()
    m.on(0, -20)
    while is_left_white() != True:
        pass
    #Finding dark blue area outside white circle
    while left_color_sensor_rli() > 50:
        pass
    m.off()
    # turning so that the right color sensor doesn't instantly sense white   
    m.on_for_rotations(-50, -40, 0.8)
    #Following edge of white circle
    Line_Flowering(left_color_sensor_rli, is_right_white, 1.5)
    #Pushing attachment into crane
    m.on_for_seconds(0, -10, 3)

def crane2tree():
    #turning and then running towards tree

    #backing into begining of circle-ish line
    m.on(0, 40)
    while not is_right_white():
        pass
    while not is_right_black():
        pass
    while not is_right_white():
        pass
    while not is_right_other_shade():
        pass
    while not is_right_white():
        pass
    m.off()
    m.on(40, 30)
    while not is_right_black():
        pass
#following circle-ish line to tree
    m.on_for_rotations(0, -30, 0.35)
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
        return mr.position - ml.position < -200
    Line_Flowering(rlidiff, stoping_point, 1.5, min_speed=-15)

    end_position = mr.position - (360 * 1.2)
    Line_Flowering(rlidiff, on_for_rotations, 1.5, stop_at_end=True)
#activating attachment to push blocks onto tree
    mmL.on_for_seconds(-75, 2)
    time.sleep(1)
    
def tree2home():
    m.on_for_rotations(0, 20, 0.5)
    m.on_for_rotations(0, 100, 1)
    m.on_for_rotations(100, -30, 1.5)
    m.on_for_seconds(0, 100, 4)
    m.on_for_seconds(-100, -50, 1)
    #while not is_right_black():
    #    pass

def Traffic_Crane():
    traffic_crane_mission()
    crane2tree()
    tree2home()


if __name__ == "__main__":
    Traffic_Crane()