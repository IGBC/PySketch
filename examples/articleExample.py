#!/usr/bin/env pysketch

def setup():
   def setup():
    pin = 18
    clock = 22
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.setup(clock, GPIO.OUT)
    GPIO.output(pin, GPIO.High)
    time.sleep(1000)
    GPIO.output(pin, GPIO.Low)

def loop():
    pass

def cleanup():
    pass
