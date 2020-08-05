"""Decorators module."""
from __future__ import annotations
import typing
from functools import wraps

from .base import html_minify


def minify_plain(remove_comments: bool = True) -> typing.Callable:
    """Minifies any function output.

    Usage:
        @minify_plain()
        def my_cool_func():
            <...>
            return some_plain_html
    """

    def compress(func: typing.Callable) -> typing.Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> typing.Any:
            return html_minify(func(*args, **kwargs), remove_comments)

        return wrapper

    return compress


def minify_disable(func: typing.Callable) -> typing.Callable:
    """Disable page minification (restricted for django).

    Usage:
        @minify_disable
        def my_cool_func():
            <...>
            return some_plain_html
    """

    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> typing.Any:
        response: typing.Any = func(*args, **kwargs)
        response.need_to_minify = False
        return response

    return wrapper
