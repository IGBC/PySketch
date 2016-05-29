import types
import importlib
from .defaults import defaults


class SketchRunner:
    __library_list = []
    __sketch = None
    __file_path = None
    __argChecker = None

    def __init__(self, sketch=None, default_library=False):
        if default_library:
            self.add_default_library()
        if sketch:
            self.set_sketch(sketch)

        # Init Arg Checker

    def add_library_item(self, item):
        # Check argument is desired type
        assert isinstance(item, str)
        self.__library_list.append(item)

    def add_default_library(self):
        self.__library_list += defaults['packageList']
        print(self.__library_list)
        # Todo: Read this in from a file or something

    def set_sketch(self, sketch):
        # Check argument is desired type
        assert isinstance(sketch, types.ModuleType)

        # if we got here then everything has passed and we can safely save data into the class
        self.__sketch = sketch

    def __register_library(self):
        """Inserts Interpreter Library of imports into __sketch in a very non-consensual way"""
        # Verify that __sketch exists, and is a module
        assert isinstance(self.__sketch, types.ModuleType)

        for list_item in self.__library_list:

            # Import the module Named in the string
            module = None
            try:
                module = importlib.import_module(list_item)

            # Hardcoded GPIO Hack
            except ImportError:
                if list_item == "RPi.GPIO":
                    from sketches import fakeGPIO
                    module = fakeGPIO
                    print("RPi.GPIO not available, you may not be running on a Pi compatible device."
                          " \nGPIO functions have been masked with stubs, so sketches can continue to function.\n")
                else:
                    raise
            if list_item == "RPi.GPIO":
                setattr(self.__sketch, "GPIO", module)
            # End Hack

            # Cram the module into the __sketch in the form of module -> "list_item", as the two are the same
            # the module matches the name, AKA the same as `import module as list_item`
            setattr(self.__sketch, list_item, module)

    def run(self, args):
        # Verify that __sketch exists, and is a module
        assert isinstance(self.__sketch, types.ModuleType)

        # Register the import library pre_execute.
        self.__register_library()

        # Try to execute setup function if it doesn't exist no one cares, just run the loop.
        try:
            self.__sketch.setup(*args)
        except AttributeError:
            pass
        # Any other error must be sent to the user.
        except:
            raise

        try:
            while True:
                self.__sketch.loop()

        # catch manual break.
        except KeyboardInterrupt:
            raise

        # If function doesn't exist catch interpreter gibbering and print meaningful error message
        except AttributeError:
            # The Loop function is optional
            pass

        # Any other error must be sent to the user.
        except:
            raise

        finally:
            # Try to call cleanup. If it doesn't exist mode along.
            try:
                self.__sketch.cleanup()
            except AttributeError:
                pass

            # Any other error must be sent to the user.
            except:
                raise
