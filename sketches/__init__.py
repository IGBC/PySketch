import inspect
import logging
import importlib
from os import path
from sys import argv
from types import ModuleType
from typing import List, Tuple

__version__ = '1.0rc1'

class SketchRunner:
    __default_package_list = [('sys', 'sys'), ('time', 'time'), ('math', 'math'), ('RPi.GPIO', 'GPIO','sketches.fakeGPIO')]

    def __init__(self, filename: str, imports: List[Tuple[str, str]] = __default_package_list):
        self.__logger = logging.getLogger('sketches.SketchRunner')
        module_path = path.abspath(filename)

        # Check file exists and is valid
        if not path.isfile(module_path):
            raise FileNotFoundError

        self.__sketch = importlib.machinery.SourceFileLoader("sketch", module_path).load_module()
        
        # get setup function and argument count
        if 'setup' in dir(self.__sketch):
            spec = inspect.getfullargspec(self.__sketch.setup)
            args = spec.args
            defaults = spec.defaults
            
            if args is None:
                args = []

            if defaults is None:
                defaults = []

            self.min_args = len(args) - len(defaults)
            # If there are no variable length arguments
            if spec.varargs is None:
                self.max_args = len(args)
            else:
                self.max_args = None
        else:
            # No setup function means min an max args are both 0
            self.max_args = 0
            self.min_args = 0

        # Register library imports into sketch
        for item in imports:
            self.__register_library(*item)

    def __register_library(self, module_name: str, attr: str, fallback: str = None):
        """Inserts Interpreter Library of imports into sketch in a very non-consensual way"""

        # Import the module Named in the string
        try:
            module = importlib.import_module(module_name)

        # If module is not found it checks if an alternative is is listed
        # If it is then it substitutes it, just so that the code can run
        except ImportError:
            if fallback is not None:
                module = importlib.import_module(fallback)
                self.__logger.warn(module_name + " not available: Replaced with " + fallback)
            else:
                self.__logger.warn(module_name + " not available: No Replacement Specified")

        # Cram the module into the __sketch in the form of module -> "attr"
        # AKA the same as `import module as attr`
        if not attr in dir(self.__sketch):
            setattr(self.__sketch, attr, module)
        else:
            self.__logger.warn(attr +" could not be imported as it's label is already used in the sketch")

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
        print(__version__)

    else:
        # Set up logger
        logger = logging.getLogger('sketches')
        ch = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s]: %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # Load File
        filename = args[0]
        params = args[1:]
		
        try:
            runner = SketchRunner(filename)
        except FileNotFoundError:
            exit("[FATAL]: Could not load " + filename)
        
        #Check Argument Count (to sketch)
        if len(params) < runner.min_args:
            exit("[FATAL]: Insufficient Arguments Supplied: Exiting")
        if len(params) > runner.max_args:
            exit("[FATAL]: Excess Arguments Supplied: Exiting")
        # Run
        runner.run(params)

