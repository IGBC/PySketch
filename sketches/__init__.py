import sys

from .runner import SketchRunner
from .moduleloader import module_loader
from .arghelper import ArgChecker


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

    args = sys.argv[1:]
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

        print("Loading " + filename)
        try:
            sketch = module_loader(filename)
        except FileNotFoundError:
            exit(filename + " not found")
        except IsADirectoryError:
            exit(filename + " is a directory")

        #Check Argument Count (to sketch)
        print("Parsing Arguments")
        args = args[1:]
        checker = ArgChecker(sketch)
        args = args[:checker.max_args]
        if not checker.verify_arg_count(len(args)):
            exit("Insufficient Arguments Supplied: Exiting")

        # Run
        runner = SketchRunner(sketch=sketch)
        print("Running Sketch")
        runner.run(args)

