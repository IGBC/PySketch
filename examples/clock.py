#!/usr/bin/env pysketch

""" Variable Freqency Square Wave Generator """

delay = 0
p = 0

def setup(freq: (float, "frequency of clock"), pin:(int, "Pin to output on") = 18):
    global delay
    global p
    delay = freq/1000
    p = pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(p, GPIO.OUT)

def loop():
    global delay
    global p
    GPIO.output(p, 1 - GPIO.input(18))
    time.sleep(delay)

def cleanup():
    GPIO.cleanup()
