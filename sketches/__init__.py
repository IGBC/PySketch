import sys
from .runner import SketchRunner
from .moduleloader import ModuleLoader
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
        exit()

    if "--help" in args:
        print(helptext)
        exit()

    if "--version" in args:
        print("TODO: Read Version" + " pre-alpha")
        exit()

    print("Loading " + args[0])
    loader = None
    try:
        loader = ModuleLoader(args[0])
    except FileNotFoundError:
        print(args[0] + " not found")
        exit()
    except IsADirectoryError:
        print(args[0] + " is a directory")
        exit()    

    print("Parsing Arguments")
    args = args[1:]
    checker = ArgChecker(loader.sketch)
    args = args[:checker.max_args]
    if not checker.verify_arg_count(args):
        print("Insufficient Arguments Supplied: Exiting")
        exit()
    return_val = -1
    try:
        runner = SketchRunner(sketch=loader.sketch)
        print("Running Sketch")
        runner.run(args)
        return_val = 0
    except AttributeError:
        print("No \"loop()\" Function found: Exiting")
    except KeyboardInterrupt:
        print("Keyboard Interrupt: Exiting")
    return return_val

