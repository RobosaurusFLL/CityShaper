#!/usr/bin/env micropython

import sys

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor

import data_calib

cleft = ColorSensor(INPUT_1)
cright = ColorSensor(INPUT_4)

def left_color_sensor_rli():
    return((cleft.reflected_light_intensity - data_calib.l_black) * 100 / (data_calib.l_white - data_calib.l_black))

def right_color_sensor_rli():
    return((cright.reflected_light_intensity - data_calib.r_black) * 100 / (data_calib.r_white - data_calib.r_black))

def is_left_white():
    if left_color_sensor_rli() > 90:
        return True
    else:
        return False

def is_left_black():
    if left_color_sensor_rli() < 10:
        return True
    else:
        return False

def is_left_not_white():
    if left_color_sensor_rli() < 50:
        return True
    else:
        return False

def is_right_white():
    if right_color_sensor_rli() > 90:
        return True
    else:
        return False

def is_right_black():
    if right_color_sensor_rli() < 10:
        return True
    else:
        return False

def is_right_not_white():
    if right_color_sensor_rli() < 90:
        return True
    else:
        return False
