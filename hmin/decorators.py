# -*- coding: utf-8 -*-
from functools import wraps

from .base import minify


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


def minify_disable(func):
    """ Disable page minification

    Usage:
        @minify_disable
        def my_cool_func():
            <...>
            return some_plain_html
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        response.need_to_minify = False
        return response
    return wrapper
