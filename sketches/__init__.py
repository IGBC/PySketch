import inspect
import importlib
from os import path
from sys import argv
from types import ModuleType
from typing import List, Tuple


class SketchRunner:
    __default_package_list = [('sys', 'sys'), ('time', 'time'), ('math', 'math'), ('RPi.GPIO', 'GPIO')]

    def __init__(self, sketch: ModuleType, imports: List[Tuple[str, str]] = __default_package_list):
        # Check argument is desired type
        if not isinstance(sketch, ModuleType):
            raise AttributeError
        self.__sketch = sketch

        # get setup function and argument count
        if 'setup' in dir(sketch):
            spec = inspect.getargspec(sketch.setup)

            args = []
            if spec.args is not None:
                args = spec.args

            defaults = []
            if spec.defaults is not None:
                defaults = spec.defaults

            # If there are no variable length arguments
            if spec.varargs is None and spec.keywords is None:
                self.max_args = len(args)
                self.min_args = len(args) - len(defaults)
            else:
                self.max_args = None
                self.min_args = len(args) - len(defaults)
        else:
            # No setup function means min an max args are both 0
            self.max_args = 0
            self.min_args = 0

        # Register library imports into sketch
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


def module_loader(filename):
    module_path = path.abspath(filename)

    # Check file exists and is valid
    if not path.isfile(module_path):
        raise FileNotFoundError

    # Catching errors here appears to be impossible, as the inner engine throws it ignoring a try/catch
    # So let it throw them, as it spits useful information to the user anyway
    try:
        return importlib.machinery.SourceFileLoader("sketch", module_path).load_module()
    except:
        raise ImportError


def main():
    helptext = ('PySketch - Write easy sketches in python.\n'
                '\n'
                'Usage:\n'
                '  pysketch (sketchfile) [sketch arguments]\n'
                '  pysketch --help\n'
                '  pysketch --version\n'
                '\n'
                'Options:\n'
                '  --help    Show this screen.\n'
                '  --version     Show version.\n'
                '\n'
                'Add "#!/usr/bin/env pysketch" to a sketchfile make it callable'
               )

    args = argv[1:]
    # Check a sketch is listed
    if len(args) == 0:
        print(helptext)

    elif "--help" in args:
        print(helptext)

    elif "--version" in args:
        print("TODO: Read Version" + " pre-alpha")

    else:
        # Load File
        filename = args[0]
        params = args[1:]
		
        print("Loading " + filename)
        try:
            sketch = module_loader(filename)
        except FileNotFoundError:
            exit("Could not load " + filename)

        runner = SketchRunner(sketch=sketch)
        #Check Argument Count (to sketch)
        if len(params) < runner.min_args:
            exit("Insufficient Arguments Supplied: Exiting")
        if len(params) > runner.max_args:
            exit("Excess Arguments Supplied: Exiting")
        # Run
        print("Running Sketch:")
        runner.run(params)

