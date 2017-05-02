# coding=utf-8

"""
Module for ArgChecker Class
"""

import inspect
from types import ModuleType


class ArgChecker:
    """
    Class for checking arguments of a sketch.
    """

    def __init__(self, sketch: ModuleType):
        if 'setup' in dir(sketch):
            spec = inspect.getargspec(sketch.setup)

            args = []
            if spec.args is not None:
                args = spec.args

            defaults = []
            if spec.defaults is not None:
                defaults = spec.defaults

            # If there are no variable length arguments
            if spec.varargs is None and spec.keywords is None:
                self.max_args = len(args)
                self.min_args = len(args) - len(defaults)
            else:
                self.max_args = None
                self.min_args = len(args) - len(defaults)
        else:
            # No setup function means min an max args are both 0
            self.max_args = 0
            self.min_args = 0

    def verify_arg_count(self, args: int):
        """
        Returns whether number of arguments supplied is correct for sketch.

        :param args: either list of args or int, to be assessed.
        :return: True if len(args) or int is appropriate for sketch.
        """

        # Calculate and return answer
        if self.max_args is None:
            return (self.max_args >= args) & (args >= self.min_args)
        else:
            return args >= self.min_args
