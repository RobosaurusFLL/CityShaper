#!/usr/bin/env micropython

import sys
import time

from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor import INPUT_2
from line import Line_Flowering, square2line
from color import *
from move import *

ml=get_left_drive_motor()
mr=get_right_drive_motor()

gyro = GyroSensor(INPUT_2)

def rlidiff():
    return (left_color_sensor_rli() - right_color_sensor_rli()) + 50

def other_stoping_point():
    return(is_left_other_shade() and is_right_other_shade()) 

def stoping_point():
    return is_left_black() and is_right_black()

def base2line():
    drive_until(is_right_other_shade, 0, -60)
    drive_until(is_right_white, -35, -40)
    drive_until(is_right_black, 0, -40)
    drive_until(is_right_white, stop_at_end=True)

    drive_for_rotations(0, -30, 0.35)
    drive_until(is_right_white, 100, -40)
    drive_until(is_right_other_shade)    

def go_2_end_of_line():
    #follow the line to the intersection
    Line_Flowering(right_color_sensor_rli, is_left_white, 1.5, min_speed=-20)
    Line_Flowering(right_color_sensor_rli, is_left_black, 1.5, min_speed=-20)
    #Line_Flowering(right_color_sensor_rli, is_left_white, 2)
    #Line_Flowering(right_color_sensor_rli, is_left_other_shade, 2, stop_at_end=True)
    drive_until(is_left_white, 0, -20)
    drive_until(is_left_other_shade)
    drive_until(is_right_other_shade, 50, -20, stop_at_end=True)
    #follow the line to the end by counting motor
    #to change amount of running to end of line / swing
    end_position = ml.position - (360 * 1.8)
    def on_for_rotations():
        return ml.position < end_position 

    Line_Flowering(right_color_sensor_rli, on_for_rotations, -2, -30)

def endofline2stability():
    #turn to stability testing mission
    drive_for_rotations(100, 20, 0.9)
    drive_for_rotations(0, -25, 0.1)
    drive_for_rotations(100, 20, 0.9)
    drive_for_rotations(0, -30, 1.3)
#to change amount of turning to safety factor
    drive_for_rotations(100, -20, 1.7)
    drive_for_seconds(0, -50, 2)
  
def stability2elevator():
    drive_for_rotations(0, 5, 0.3)
    drive_until(is_left_white, 0, 30)
    drive_until(is_left_black)
    drive_until(is_left_white, stop_at_end=True)

    Line_Flowering(rlidiff, other_stoping_point, 1.5, min_speed=-20, stop_at_end=True)
    #Turing around
    drive_for_rotations(0, -10, 0.3)
    drive_until(is_right_white, 100, -30)
    drive_until(is_right_black)
    drive_until(is_right_white, stop_at_end=True)

    Line_Flowering(rlidiff, stoping_point, 1.5, -50, min_speed=-20, stop_at_end=True)
    drive_for_rotations(0, -20, 0.5)
    drive_until(is_right_white, 100, -30)
    drive_until(is_right_black)
    drive_until(is_right_white, stop_at_end=True)

def ramp_mission():
    Line_Flowering(rlidiff, stoping_point, 1.5, -50, min_speed=-20, stop_at_end=True)

    def gyro_on_ramp():
        return st - 10 > gyro.angle
    def gyro_on_flat():
        return st - 5 < gyro.angle

    st = gyro.angle
    drive_until(gyro_on_ramp, 0, -30)
    drive_until(gyro_on_flat)

    drive_for_rotations(0, -20, 0.5)
    drive_for_rotations(100, -10, 0.6)

def swing2ramp():
    base2line()
    go_2_end_of_line()
    endofline2stability()
    stability2elevator()
    ramp_mission()

if __name__ == "__main__":
    swing2ramp()
