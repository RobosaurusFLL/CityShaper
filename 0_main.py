#!/usr/bin/env micropython

import sys
import time

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.motor import LargeMotor, MoveTank, MoveSteering
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_2
from line import Line_Flowering, square2line, square2Otherline
from color import *

from ev3dev2.button import Button
from time import sleep
from push_blocks import push2redcircle, push2blackcircle
from swing2ramp import swing2ramp
from Traffic_Crane import Traffic_Crane

import os
os.system('setfont Lat15-TerminusBold32x16')

btn = Button()

function_list = [push2blackcircle, push2redcircle, Traffic_Crane, swing2ramp]
func_index = -1

prev_butt = []
print("Ready")
while True:
    butt = btn.buttons_pressed
    if prev_butt != butt:
        #print(str(prev_butt) + " -> "+ str(butt), file=sys.stderr)
        if len(butt) == 0:
            #print(prev_butt[0] + " released", file=sys.stderr)
            if prev_butt[0] == "enter":
                func_index = func_index + 1
            if prev_butt[0] == "up":
                func_index = 0
            if prev_butt[0] == "right":
                func_index = 1
            if prev_butt[0] == "down":
                func_index = 2
            if prev_butt[0] == "left":
                func_index = 3
            if func_index >= 0 and func_index < len(function_list):
                function_list[func_index]()
        prev_butt = butt
    sleep(0.01)

