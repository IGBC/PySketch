#!/usr/bin/env pysketch

i = 0

def setup(arg):
    print("setup("+arg+")")

def loop():
    global i
    i = i + 1
    print("loop: " + str(i))
    time.sleep(1)

def cleanup():
    print("cleanup")
