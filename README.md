# PySketch
Interpreter for Arduino style python sketches
## About 
PySketch is an interpreter for python "sketches". The name sketch is taken from the short C programs that the Arduino IDE complies and uploads to Ardunio devices. Arduino sketches have a fixed format: a `setup()` function that is run once and a `loop()` function that is then run repeatedly forever. This format makes it easy to start writing simple C applications to control the device. 

PySketch uses the same format, allowing you to write simple programs to perform every day tasks, for example controlling a Raspberry Pi's GPIO, with almost no boilerplate code. The best way to demonstrate this is probably with an example. Read the comments for explanation:
```python
#!/usr/bin/pysketch

# Blinky.py - Sketch to blink an LED on an RPi
# This script assumes you have an LED connected from pin 12 to GND. (Via a resistor plz)

def setup(argv): # This code is automatically executed when the sketch starts.
  GPIO.setmode(GPIO.BCM) # The RPi.GPIO Library is automatically loaded in.
  GPIO.setup(18, GPIO.OUT) 
  
def loop(): # This Code runs in a loop until it calls exit() or crashes or a keyboardInterrupt event is fired.
  GPIO.output(18, 1 - GPIO.input(18))
  time.sleep(1) # time automatically loaded in.
  
def cleanup(): # This is called at the end, regardless of how loop() exits, even if it crashes.
  GPIO.cleanup()
```
  
Now look at the equivalent vanilla python:
```python
#!/usr/bin/python3

# Blinky.py - Script to blink an LED on an RPi
# This script assumes you have an LED connected from pin 12 to GND. (Via a resistor plz)

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

try
  while true:
    GPIO.output(18, 1 - GPIO.input(18))
    time.sleep(1)
except keyboadInterrupt:
  print("Keyboard Interrupt: Exiting")
except:
  raise
finally:
  GPIO.cleanup()  
```
(Ignoring comments and whitespace) The vanilla python script is 15 lines of code, the sketch is only 9. There are 5 lines of functional code in these programs, meaning in the sketch there is only 4 lines of boilerplate code, in the simple blink program there are 10*.

*Ironically to eliminate those 10 lines the interpreter is over 120 lines long.
