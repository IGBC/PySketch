import logging
import importlib
import argparse
from os import path
from sys import argv
from typing import List, Tuple

__version__ = '1.1beta1'

class SketchRunner:
    __default_package_list = [('sys', 'sys'), ('time', 'time'), ('math', 'math'), ('RPi.GPIO', 'GPIO','sketches.fakeGPIO')]

    def __init__(self, filename: str, imports: List[Tuple[str, str]] = __default_package_list):
        self.__logger = logging.getLogger('sketches.SketchRunner')
        self.__filename = filename
        module_path = path.abspath(filename)

        # Check file exists and is valid
        if not path.isfile(module_path):
            self.__logger.fatal("Could not load '{}': file not found".format(module_path))
            raise FileNotFoundError

        self.__sketch = importlib.machinery.SourceFileLoader("sketch", module_path).load_module()

        self.__parser = argparse.ArgumentParser(description=self.__sketch.__doc__)
        self.__parser.add_argument(filename, help="This sketchfile")

        # Read setup() annotations and give them to argparse
        if 'setup' in dir(self.__sketch):
            fun = self.__sketch.setup
            args = fun.__code__.co_varnames[:fun.__code__.co_argcount]
            defaults = { n: v for n, v in zip(reversed(args), reversed(fun.__defaults__)) }
            for n in args:
                annotation = fun.__annotations__.get(n,str)
                if not isinstance(annotation, (tuple, list)):
                    annotation = (annotation, "")
                helpstr = "{} {} {}".format(annotation[1],annotation[0], " (default: %(default)s)" if n in defaults else "")
                self.__parser.add_argument(n, type=annotation[0], nargs=('?' if n in defaults else None), default=defaults.get(n), help=helpstr)

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
            # Get argparse wrapper for setup
            params = self.__parser.parse_args([self.__filename] + args).__dict__
            params.pop(self.__filename)
            self.__sketch.setup(**params)
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
    parser = argparse.ArgumentParser(description='PySketch - Write easy sketches in python.\n'
                                                 'Add "#!/usr/bin/env pysketch" to a sketchfile and make it executable to run from the shell')
    parser.add_argument('sketchfile', type=str, help="file to load and execute")
    parser.add_argument('sketch arguments', nargs=argparse.REMAINDER, help="arguments to the sketch")
    parser.add_argument('-v, --version', action='version', version=__version__)
    # Set up logger
    logger = logging.getLogger('sketches')
    ch = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s]: %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    args = parser.parse_args().__dict__
    try:
        runner = SketchRunner(args['sketchfile'])
    except FileNotFoundError:
        exit()

    runner.run(args['sketch arguments'])

