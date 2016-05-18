#!/usr/bin/python3

import os
import sys
from importlib.machinery import SourceFileLoader

# Library imports (Imports only for use in the sketches library)
import time
# try to import RPi.GPIO if is available
try:
    import RPi.GPIO as GPIO
    print("RPi.GPIO Loaded")
except ImportError:
    print("todo mask GPIO")
    # import GPIO masking library so sketch still functions
    # import fake.RPi.GPIO as GPIO # uncomment when available.
    GPIO = 0
    print("RPi.GPIO not available, you may not be running on a Pi compatible device. \nGPIO functions have been "
          "masked with stubs, so sketches can continue to function.\n")

usage_text = "Usage: \n   sketch_runner.py \"sketch filename\" [arguments for sketch] \n   Add " \
             "\"#!/path/to/sketch_runner.py\" to sketches to make them executable"

# runner code
if __name__ == "__main__":
    # If not enough arguments
    if len(sys.argv) == 1:
        print(usage_text + "\n")
        exit()

    module_path = os.path.abspath(sys.argv[1])

    # Check file exists and is valid

    if not os.path.exists(module_path):
        print("File " + module_path + " not found" + "\n")
        exit()

    if not os.path.isfile(module_path):
        print(module_path + " is a directory" + "\n")
        exit()

    print("Importing: " + module_path + "\n")

    # Catching errors here appears to be impossible, as the inner engine throws it ignoring a try/catch
    # So let it throw them, as it spits useful information to the user anyway
    sketch = SourceFileLoader("sketch", module_path).load_module()

    # Forcibly jam the interpreters libraries down the sketches throat
    setattr(sketch, "sys", sys)
    setattr(sketch, "time", time)
    setattr(sketch, "GPIO", GPIO)

    # Try to execute setup function if it doesn't exist no one cares, just run the loop.
    try:
        sketch.setup(sys.argv[2:])
    except AttributeError:
        pass
    # Any other error must be sent to the user.
    except:
        raise

    print("Running sketch" + "\n")

    try:
        while True:
            sketch.loop()

    # catch manual break.
    except KeyboardInterrupt:
        print("Keyboard Interrupt: Exiting")

    # If function doesn't exist catch interpreter gibbering and print meaningful error message
    except AttributeError:
        print("No \"loop()\" Function found. Exiting")

    # Any other error must be sent to the user.
    except:
        raise

    finally:
        # Try to call cleanup. If it doesn't exist mode along.
        try:
            sketch.cleanup()
        except AttributeError:
            pass

        # Any other error must be sent to the user.
        except:
            raise

