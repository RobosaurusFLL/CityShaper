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
mmR=get_right_action_motor()

gyro = GyroSensor(INPUT_2)

def rlidiff():
    #using difference of the 2 color sensors to follow the middle of the line
    return (left_color_sensor_rli() - right_color_sensor_rli()) + 50

def stoping_point():
    #stopping when both color sensors sense black
    return is_left_black() and is_right_black()

def base2line():
    #driving out of base and turning to the line
    drive_staight(is_right_other_shade, -60, -10)
    drive_until(is_right_white, -35, -40)
 
def line2red_circle():
    end_position = mr.position - (360 * 1)
    def on_for_rotations():
        return mr.position < end_position
    #following line to the slightly turning point
    Line_Flowering(rlidiff, on_for_rotations, 1.5, min_speed=-20)
    Line_Flowering(rlidiff, is_right_black, 1, max_speed=-60, stop_at_end=True)

def release_cake_truck():
    #lifting box and driving forwards to recapture tan blocks
    mmL.on_for_seconds(75, 0.5)
    drive_for_rotations(0, -20, 0.8)
    mmL.on_for_seconds(-75, 0.5)

def red_circle2end_of_line():
    #following line until reaching the branching out line
    Line_Flowering(right_color_sensor_rli, is_left_white, 1.5, min_speed=-20)
    Line_Flowering(right_color_sensor_rli, is_left_black, 1.5, min_speed=-20)
    Line_Flowering(right_color_sensor_rli, is_left_white, 1.5, min_speed=-20)
    def on_for_rotations():
        return mr.position < end_position 

    end_position = mr.position - (360 * 0.5)
    Line_Flowering(right_color_sensor_rli, on_for_rotations, 1.5, min_speed=-20)
    #driving slightly left to avoid catching on the pole of the swing
    drive_for_rotations(-5, -50, 1)
    #turning against the pole of the swing and pushing attachment into safety factor
    drive_for_seconds(50, -100, 1.5)
    #"wiggling" to make sure the attachment is pushed into the safety factor
    drive_for_seconds(0, -100, 0.5)

def line2elevator():
    #backing past branching out line
    drive_for_rotations(0, 50, 3.5)
    #finding way to line next to the elevator by wiggling a lot
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
    #following line into elevator & pushing into it
    Line_Flowering(right_color_sensor_rli, on_for_seconds, -2, stop_at_end=True)

def release_tan_blocks():
    # lifting box again to release tan blocks into tan circle
    mmL.on_for_seconds(75, 0.5)
    #backing out
    drive_for_rotations(50, 40, 1)
    drive_until(is_left_white, -100, -40)
    drive_until(is_left_black)
    drive_until(is_left_white, stop_at_end=True)

def ramp_mission():
    #following line to bottom of the ramp
    Line_Flowering(rlidiff, stoping_point, 1.5, -50, min_speed=-20, stop_at_end=True)
    drive_for_rotations(0, -40, 0.2)
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
    #driving up ramp, using tilt of the gyro sensor to sense when we reach the top
    drive_until(gyro_on_ramp, 0, -30)
    drive_until(gyro_on_flat)
    #rotating a little to raise flags
    drive_for_rotations(0, -20, 0.5)
    drive_for_rotations(100, -10, 0.6)
    mmL.on_for_seconds(-75, 1.5)
    mmR.on_for_seconds(-50, 2)

def swing2ramp():
    #combining all the sections' function
    base2line()
    line2red_circle()
    release_cake_truck()
    red_circle2end_of_line()
    line2elevator()
    release_tan_blocks()
    ramp_mission()

if __name__ == "__main__":
    swing2ramp()
