#!/usr/bin/env pysketch

""" This sketch emulates a time wasteing tool """

from typing import List

sys = 0

def setup(a:tuple, b:[float, 32.34212], c, d:int = 4):
    print("setup("+arg+")")
    print(dir())

def loop():
    global sys
    sys = sys + 1
    print("loop: " + str(sys))
    time.sleep(1)

def cleanup():
    print("cleanup")
