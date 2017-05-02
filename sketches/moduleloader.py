from os import path
from importlib.machinery import SourceFileLoader


def module_loader(filename):
    module_path = path.abspath(filename)

    # Check file exists and is valid
    if not path.isfile(module_path):
        raise FileNotFoundError

    # Catching errors here appears to be impossible, as the inner engine throws it ignoring a try/catch
    # So let it throw them, as it spits useful information to the user anyway
    try:
        return SourceFileLoader("sketch", module_path).load_module()
    except:
        raise ImportError
