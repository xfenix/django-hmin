# -*- coding: utf-8 -*-
from functools import wraps

try:
    from .base import minify
except ImportError:
    from .base2 import minify


def minify_plain(remove_comments=True):
    """ Minifies any function output

    Usage:
        @minify_plain()
        def my_cool_func():
            <...>
            return some_plain_html
    """
    def compress(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return  minify(func(*args, **kwargs), remove_comments)
        return wrapper
    return compress
