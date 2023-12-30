"""Code for test_extract_names.py."""

import os  # noqa
from sys import path as sys_path  # noqa

import backoff

FOO = 123


@backoff.on_exception(backoff.expo, Exception, max_tries=8)
def foo():
    """Foo docstring."""
    pass


async def bar():
    """Bar docstring."""
    pass


class MyClass:
    """MyClass docstring."""

    class_attr = 42

    def method(self):
        """Method docstring."""
        pass

    @staticmethod
    def static_method(a, b):
        """Static method docstring."""
        return a + b

    @classmethod
    def class_method(cls):
        """Class method docstring."""
        pass
