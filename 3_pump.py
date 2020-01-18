#!/usr/bin/env micropython

import sys
import time

from move import *
ml = get_left_action_motor()
mr = get_right_action_motor()

mr.on(100)
while True:
    pass