from .runner import SketchRunner as SketchRunner


def interpreter(args):
    if len(args) == 0:
        print('Usage: \n   sketch_runner.py "sketch filename" [arguments for sketch] \n   Add'
              ' "#!/path/to/sketch_runner.py" to sketches to make them executable')
        return -2


    return_val = -1
    try:
        print("Loading " + args[0])
        runner = SketchRunner(sketch=args[0], default_library=True)
        print("Running Sketch \n")
        runner.run(args[1:])
        return_val = 0
    except FileNotFoundError:
        print(args[0] + " not found \n")
    except IsADirectoryError:
        print(args[0] + " is a directory \n")
    except AttributeError:
        print("No \"loop()\" Function found. Exiting")
    except KeyboardInterrupt:
        print("Keyboard Interrupt: Exiting")
    return return_val
