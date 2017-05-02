#!/usr/bin/env pysketch

sys = 0

def setup(arg):
    print("setup("+arg+")")
    print(dir())

def loop():
    global sys
    sys = sys + 1
    print("loop: " + str(sys))
    time.sleep(1)

def cleanup():
    print("cleanup")
