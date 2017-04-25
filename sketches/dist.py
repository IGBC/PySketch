import os, sys, importlib, inspect

def get_dist(submodules):
    dist = {}

    for path in get_path():
        dir_mod = get_modules(path)
        for mod, file in dir_mod.items():
            dist[mod] = file
    dist = sorted(dist.items())
    if not submodules:
    	dist = [d for d in dist if '.' in d]
    return dist

def get_path():
    # Get python lookup locations
    path = list(map(os.path.normcase, map(os.path.abspath, sys.path[:])))
    cwd = os.getcwd()
    for p in path:
	# Remove nonexistant dirs and working dir from list
        if (not os.path.isdir(p)) or (p == cwd):
            path.remove(p)
    return path

def get_modules(dir):
    modules = {}
    # Get all files in the given directory
    try:
        files = os.listdir(dir)
    except:
        # I guess not then
        return modules # WHich is empty
    for file in files:
        fname = os.path.join(dir, file)
        if os.path.isfile(fname):
            module = inspect.getmodulename(fname)
            if module:
                modules[module] = fname
        elif os.path.isdir(fname):
            dir_modules = __try_import_dir(fname)
            # Extract modules from dir
            for m, f in dir_modules.items():
                modules[m] = f
    return modules

def __try_import_dir(dir):
    modules = {}
    # Get module name
    module = os.path.basename(dir)
    # Check dir has valid module in it
    if os.path.isfile(os.path.join(dir, "__init__.py")):
        # Recursively check this directory
        dir_modules = get_modules(dir)
        for submodule, file in dir_modules.items():
            if submodule == "__init__":
                modules[module] = file
            else:
                modules[module + "." + submodule] = file
                pass
    return modules
