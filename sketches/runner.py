import importlib
from types import ModuleType
from typing import List


class SketchRunner:

    __default_package_list = ['sys', 'time', 'math', 'RPi.GPIO']

    def __init__(self, sketch: ModuleType, imports: List[str] = __default_package_list):
        # Check argument is desired type
        if not isinstance(sketch, ModuleType):
            raise AttributeError
        self.__sketch = sketch

        for item in imports:
            self.__register_library(item)

    def __register_library(self, item: str):
        """Inserts Interpreter Library of imports into sketch in a very non-consensual way"""

        # Import the module Named in the string
        module = None
        try:
            module = importlib.import_module(item)

        # Hardcoded GPIO Hack
        # If module is not found it checks if it is the RPi.GPIO module. (Not available on PC's)
        # If it is then it substitutes it for a fake stub version, just so that the code can run
        except ImportError:
            if item == "RPi.GPIO":
                from sketches import fakeGPIO
                module = fakeGPIO
                print("\nRPi.GPIO not available, you may not be running on a Pi compatible device."
                      "\nGPIO functions have been masked with stubs, so sketches can continue to function.\n")
            else:
            # If the module is not GPIO raise the import error, after all the user just tried to load a module that
            # Doesn't exist.
                raise

        # This hack fakes around "import RPi.GPIO as GPIO" which is what all the GPIO demos (and thus everyone else)
        # does. If you can't beat 'em join 'em
        if item == "RPi.GPIO":
            setattr(self.__sketch, "GPIO", module)
        # End Hack

        # Cram the module into the __sketch in the form of module -> "item", as the two are the same
        # the module matches the name, AKA the same as `import module as item`
        setattr(self.__sketch, item, module)

    def run(self, args):
        # Try to execute setup function if it doesn't exist no one cares, just run the loop.
        if 'setup' in dir(self.__sketch):
            self.__sketch.setup(*args)

        try:
            if 'loop' in dir(self.__sketch):
                while True:
                    self.__sketch.loop()

        # Swallow the user pressing ^C, we're expecting that.
        except KeyboardInterrupt:
            pass

        # Shout about everything else.
        except:
            raise

        finally:
            # Try to call cleanup. If it doesn't exist move along.
            if 'cleanup' in dir(self.__sketch):
                self.__sketch.cleanup()

