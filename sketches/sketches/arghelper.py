# coding=utf-8

"""
Module for ArgChecker Class
"""

import inspect
import types


class ArgChecker:
    """
    Class for checking arguments of a sketch.
    """
    __sketch = None
    min_args = 0
    max_args = None

    def __init__(self, sketch):
        assert isinstance(sketch, types.ModuleType)
        self.__sketch = sketch
        try:
            setup_function = sketch.setup
        except AttributeError:
            # setup function is optional so just return
            return

        spec = inspect.getargspec(setup_function)

        args = []
        if spec.args is not None:
            args = spec.args

        defaults = []
        if spec.defaults is not None:
            defaults = spec.defaults

            # If there are no variable length arguments
        if (spec.varargs is None) and (spec.keywords is None):
            self.max_args = len(args)
            self.min_args = len(args) - len(defaults)
        else:
            self.min_args = len(args) - len(defaults)

    def verify_arg_count(self, args):
        """
        Returns whether number of arguments supplied is correct for sketch.
        :param args: either list of args or int, to be assessed.
        :return: True if len(args) or int is appropriate for sketch.
        """

        # Convert list into its length
        if isinstance(args, list):
            args = len(args)

        # Verify that we now have an int
        assert isinstance(args, int)

        # Calculate and return answer
        if self.max_args is None:
            return (self.max_args >= args) & (args >= self.min_args)
        else:
            return args >= self.min_args
