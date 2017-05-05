import sys

from .runner import SketchRunner
from .moduleloader import module_loader


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

