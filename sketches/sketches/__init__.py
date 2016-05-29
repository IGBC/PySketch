from .runner import SketchRunner
from .moduleloader import ModuleLoader
from .arghelper import ArgChecker


class Interpreter:
    loader = None
    checker = None
    args = []

    def __init__(self, args):
        # Check a sketch is listed
        if len(args) == 0:
            print('Usage: \n   sketch_runner.py "__sketch filename" [arguments for __sketch] \n   Add'
                  ' "#!/path/to/sketch_runner.py" to sketches to make them executable')
            exit()

        print("Loading " + args[0])
        self.__load_file(args[0])
        print("Parsing Arguments")
        self.__fix_args(args[1:])
        self.__run()

    def __load_file(self, file):
        try:
            self.loader = ModuleLoader(file)
        except FileNotFoundError:
            print(file + " not found \n")
        except IsADirectoryError:
            print(file + " is a directory \n")

    def __fix_args(self, args):
        assert isinstance(args, list)
        self.checker = ArgChecker(self.loader.sketch)
        self.args = args[:self.checker.max_args]
        if not self.checker.verify_arg_count(self.args):
            print("Insufficient Arguments Supplied: Exiting")
            exit()

    def __run(self):
        return_val = -1
        try:
            runner = SketchRunner(sketch=self.loader.sketch, default_library=True)
            print("Running Sketch \n")
            runner.run(self.args)
            return_val = 0
        except AttributeError:
            print("No \"loop()\" Function found: Exiting")
        except KeyboardInterrupt:
            print("Keyboard Interrupt: Exiting")
        return return_val
