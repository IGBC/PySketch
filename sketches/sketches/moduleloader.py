import os
from importlib.machinery import SourceFileLoader


class ModuleLoader:
    sketch = None
    module_path = None

    def __init__(self, file):
        self.load_sketch(file)

    def load_sketch(self, file):
        module_path = os.path.abspath(file)

        # Check file exists and is valid
        if not os.path.exists(module_path):
            raise FileNotFoundError

        if not os.path.isfile(module_path):
            raise IsADirectoryError

        # Catching errors here appears to be impossible, as the inner engine throws it ignoring a try/catch
        # So let it throw them, as it spits useful information to the user anyway
        try:
            sketch = SourceFileLoader("sketch", module_path).load_module()
        except:
            raise ImportError

        # If we get here everything is good so commit the data to the class
        self.sketch = sketch
        self.module_path = module_path
