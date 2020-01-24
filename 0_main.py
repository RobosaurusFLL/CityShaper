#!/usr/bin/env micropython

#This program is run durring the robotic competition, and reacts whenever a 
# certain button is pressed by running the mission corrosponding to that button. 
#If only the middle button is pressed, it will run the missions in a pre definned order
import sys
import time

from ev3dev2.button import Button
from time import sleep
from push_blocks import blocks_and_crane
from swing2ramp import swing2ramp
from Traffic_Tree import Traffic_Tree

import os
os.system('setfont Lat15-TerminusBold32x16')

from move import *
ml = get_left_action_motor()
mr = get_right_action_motor()

btn = Button()

function_list = [blocks_and_crane, Traffic_Tree, swing2ramp]
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
                ml.off(brake=False)
                mr.off(brake=False)
        prev_butt = butt
    sleep(0.01)

