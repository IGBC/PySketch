import os
import types
import importlib
from importlib.machinery import SourceFileLoader


class SketchRunner:
    __library_list = []
    __sketch = None
    __file_path = None

    def __init__(self, sketch=None, default_library=False):
        if default_library:
            self.add_default_library()
        if sketch:
            self.set_sketch(sketch)

    def add_library_item(self, item):
        # Check argument is desired type
        assert isinstance(item, types.string)
        self.__library_list.append(item)

    def add_default_library(self):
        self.__library_list.append(['sys', 'time', 'RPi.GPIO'])
        # Todo: Read this in from a file or something

    def set_sketch(self, sketch):
        # Check argument is desired type
        assert isinstance(sketch, types.string)

        module_path = os.path.abspath(sketch)

        # Check file exists and is valid
        if not os.path.exists(module_path):
            raise FileNotFoundError

        if not os.path.isfile(module_path):
            raise IsADirectoryError

        # Catching errors here appears to be impossible, as the inner engine throws it ignoring a try/catch
        # So let it throw them, as it spits useful information to the user anyway
        sketch = SourceFileLoader("sketch", module_path).load_module()

        assert isinstance(sketch, types.ModuleType)

        # if we got here then everything has passed and we can safely save data into the class
        self.__file_path = module_path
        self.__sketch = sketch

    def __register_library(self):
        """Inserts Interpreter Library of imports into sketch in a very non-consensual way"""
        # Verify that sketch exists, and is a module
        assert isinstance(self.__sketch, types.ModuleType)

        for list_item in self.__library_list:

            # Import the module Named in the string
            module = importlib.import_module(list_item)
            # Cram the module into the sketch in the form of module -> "list_item", as the two are the same
            # the module matches the name, AKA the same as `import module as list_item`
            setattr(self.__sketch, list_item, module)

    def run(self, args):
        # Verify that sketch exists, and is a module
        assert isinstance(self.__sketch, types.ModuleType)

        # Register the import library pre_execute.
        self.__register_library()

        # Try to execute setup function if it doesn't exist no one cares, just run the loop.
        try:
            self.__sketch.setup(args)
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
            print("Keyboard Interrupt: Exiting")

        # If function doesn't exist catch interpreter gibbering and print meaningful error message
        except AttributeError:
            print("No \"loop()\" Function found. Exiting")

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
