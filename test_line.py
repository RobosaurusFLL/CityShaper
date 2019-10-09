#!/usr/bin/env micropython

import sys
import time

import os
os.system('setfont Lat15-TerminusBold32x16')

from line import Line_Flowering, square2line
from color import *

#Line_Flowering(right_color_sensor_rli, is_left_white, 2, -50)

square2line()