Sketches
========

Write Arduino style sketches in Python

About
-----

Sketches allows users to write simple "sketches" in python for performing every day simple computation, without having to worry about much of the 'boilerplate' code that a typical python script requires. The name sketch is taken from the short C programs that the Arduino IDE complies and uploads to Arduino devices. Arduino sketches have a fixed format: a `setup()` function that is run once and a `loop()` function that is then run repeatedly forever. This format makes it easy to start writing simple programs to control the device. 

Sketches uses the same format, allowing you to write simple programs to perform every day tasks, for example controlling a Raspberry Pi's GPIO, with almost no boilerplate code. 

Features
--------

* **Write low overhead sketch files:** For a functioning sketch you only have to define the interpreter and at one of `setup()`, `loop()`, or `cleanup()` and you're ready to code.
* **Automatic imports:** Sketches will automatically import a selection of commonly used libraries at runtime, meaning you don't have to worry about your import statements.
* **Argument Preparsing:** Sketches will before running your code check the input arguments to ensure the right number of arguments are passed to your script, so you don't have to write code to check they're all there. Simply define the arguments you want as the parameters of your `setup()` function.
* **Clean crashing:** When your code is stopped by user interupt, or otherwise crashes `cleanup()` is run, giving you the opportunity to safely end your program.
* **Error Reporting:** Errors your code throws are printed back to the terminal so you can see where it broke.

Examples
--------

The best way to demonstrate this is probably with an example. Read the comments for explanation:

.. code:: python

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

  
Now look at the equivalent vanilla python:

.. code:: python

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
    except keyboardInterrupt:
        print("Keyboard Interrupt: Exiting")
    except:
        raise
    finally:
        GPIO.cleanup()  

(Ignoring comments and whitespace) The vanilla python script is 15 lines of code, the sketch is only 9. There are 5 lines of functional code in these programs, meaning in the sketch there is only 4 lines of boilerplate code, in the simple blink program there are 10*.

*Ironically to eliminate those 10 lines the interpreter is over 120 lines long.

Installation:
-------------

Sketches is packaged at PyPI (Python Package Index), so install it using `pip3`. This package is only provided for python 3 (3.4 officially supported)

Install:
``` bash
pip3 install sketches
```

Usage
-----

Add `#!/usr/bin/pysketch` to the top of your file, then run `./<filename> [args]`.

Or run `pysketch <filename> [args]`

Why?
----

In my day job I found myself writing a large number of scripts on the Raspberry Pi that had a surprisingly similar format: 
- set up variables
- while True do something
- on keyboard exception: clean up resources.

I wondered if there was a framework to automate away a lot of the boilerplate. When I didn't find one I wrote a template python file. As that started to get long, I wrote Sketches.
