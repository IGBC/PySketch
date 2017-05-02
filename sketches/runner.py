import importlib
from types import ModuleType
from typing import List, Tuple


class SketchRunner:

    __default_package_list = [('sys', 'sys'), ('time', 'time'), ('math', 'math'), ('RPi.GPIO', 'GPIO')]

    def __init__(self, sketch: ModuleType, imports: List[Tuple[str, str]] = __default_package_list):
        # Check argument is desired type
        if not isinstance(sketch, ModuleType):
            raise AttributeError
        self.__sketch = sketch

        for item in imports:
            self.__register_library(item[0], item[1])

    def __register_library(self, module_name: str, attr: str):
        """Inserts Interpreter Library of imports into sketch in a very non-consensual way"""

        # Import the module Named in the string
        try:
            module = importlib.import_module(module_name)

        # Hardcoded GPIO Hack
        # If module is not found it checks if it is the RPi.GPIO module. (Not available on PC's)
        # If it is then it substitutes it for a fake stub version, just so that the code can run
        except ImportError:
            if module_name == "RPi.GPIO":
                from sketches import fakeGPIO
                module = fakeGPIO
                print("\nRPi.GPIO not available, you may not be running on a Pi compatible device."
                      "\nGPIO functions have been masked with stubs, so sketches can continue to function.\n")
            else:
            # If the module is not GPIO raise the import error, after all the user just tried to load a module that
            # Doesn't exist.
                raise

        # Cram the module into the __sketch in the form of module -> "attr"
        # AKA the same as `import module as attr`
        if not attr in dir(self.__sketch):
            setattr(self.__sketch, attr, module)
        else:
            print("\n"+ attr +" could not be imported as it's label is already used in the sketch")

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

