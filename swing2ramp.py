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
mmL=get_left_action_motor()

gyro = GyroSensor(INPUT_2)

def rlidiff():
    return (left_color_sensor_rli() - right_color_sensor_rli()) + 50

def other_stoping_point():
    return(is_left_other_shade() and is_right_other_shade()) 

def stoping_point():
    return is_left_black() and is_right_black()

def base2line():
    drive_staight(is_right_other_shade, -60, -10)
    drive_until(is_left_white, -100, -20)
    drive_until(is_right_white, 0, -40)
    drive_until(is_right_black, 0, -40)
    drive_until(is_right_white, stop_at_end=True)
    drive_for_rotations(0, -30, 0.35)
    drive_until(is_right_white, 100, -40)
    drive_until(is_right_black)    
    drive_until(is_right_white, stop_at_end=True)    

def line2red_circle():
    end_position = mr.position - (360 * 1.5)
    def on_for_rotations():
        return mr.position < end_position

    Line_Flowering(rlidiff, on_for_rotations, 1.5, min_speed=-20)
    Line_Flowering(rlidiff, is_right_black, 1.5, stop_at_end=True)

def release_cake_truck():
    mmL.on_for_seconds(-75, 1)
    drive_for_rotations(0, -20, 0.4)
    mmL.on_for_seconds(75, 1)

def red_circle2end_of_line():
    drive_for_rotations(0, -20, 0.5)
    Line_Flowering(right_color_sensor_rli, is_left_white, 1.5, min_speed=-20)
    Line_Flowering(right_color_sensor_rli, is_left_black, 1.5, min_speed=-20)
    Line_Flowering(right_color_sensor_rli, is_left_white, 1.5, min_speed=-20)
    def on_for_rotations():
        return mr.position < end_position 

    end_position = mr.position - (360 * 1)
    Line_Flowering(right_color_sensor_rli, on_for_rotations, 1.5, min_speed=-20)
    drive_for_rotations(-5, -50, 1)
    drive_for_seconds(50, -100, 1)
    drive_for_seconds(0, -100, 0.5)

def line2elevator():
    drive_for_rotations(0, 50, 3.5)
    drive_until(is_left_white, -40, -40)
    drive_until(is_left_black)
    drive_until(is_left_white)
    drive_until(is_left_other_shade)
    drive_until(is_right_other_shade)
    drive_until(is_left_white, 50, 40)
    drive_until(is_left_black, stop_at_end=True)
    Line_Flowering(left_color_sensor_rli, is_right_other_shade, -2, max_speed=-30)
    Line_Flowering(left_color_sensor_rli, is_right_white, -2, max_speed=-30)
    Line_Flowering(left_color_sensor_rli, is_right_black, -2)
    Line_Flowering(left_color_sensor_rli, is_right_white, -2)
    Line_Flowering(left_color_sensor_rli, is_right_other_shade, -2)
    drive_until(is_right_white, 100, -40)
    #when2stop = current time + goal
    end_time = time.time() + 7
    def on_for_seconds():
        return time.time() > end_time
    Line_Flowering(right_color_sensor_rli, on_for_seconds, -2, stop_at_end=True)

def release_tan_blocks():
    mmL.on_for_seconds(-75, 1)
    drive_for_rotations(50, 40, 1)
    drive_until(is_left_white, -100, -40)
    drive_until(is_left_black)
    drive_until(is_left_white, stop_at_end=True)

def ramp_mission():
    Line_Flowering(rlidiff, stoping_point, 1.5, -50, min_speed=-20, stop_at_end=True)
    drive_for_rotations(0, -40, 0.5)
    drive_until(is_right_white, 100, -40)
    drive_until(is_right_black)
    drive_until(is_right_white, stop_at_end=True)

    Line_Flowering(rlidiff, stoping_point, 1.5, -50, min_speed=-20, stop_at_end=True)
    gyro._ensure_mode(GyroSensor.MODE_TILT_ANG)
    def gyro_on_ramp():
        return st - 10 > gyro.tilt_angle
    def gyro_on_flat():
        return st - 5 < gyro.tilt_angle

    st = gyro.tilt_angle
    drive_until(gyro_on_ramp, 0, -30)
    drive_until(gyro_on_flat)

    drive_for_rotations(0, -20, 0.5)
    drive_for_rotations(100, -10, 0.6)

def swing2ramp():
    base2line()
    line2red_circle()
    release_cake_truck()

    red_circle2end_of_line()
    line2elevator()
    release_tan_blocks()
    ramp_mission()

if __name__ == "__main__":
    swing2ramp()

