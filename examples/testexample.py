#!/usr/bin/env pysketch
from typing import List

sys = 0

def setup(a:str, b:float, c, d:int = 4):
    print("setup("+arg+")")
    print(dir())

def loop():
    global sys
    sys = sys + 1
    print("loop: " + str(sys))
    time.sleep(1)

def cleanup():
    print("cleanup")
