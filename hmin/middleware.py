"""Django middleware."""
from __future__ import annotations
import logging
import re
import typing

from django.conf import settings
from django.core.cache import InvalidCacheBackendError, caches
from django.core.cache.backends.base import BaseCache
from django.http import HttpRequest, HttpResponse

from .base import html_minify


hash_func: typing.Callable
try:
    import xxhash

    hash_func = xxhash.xxh64
except ImportError:
    import hashlib

    hash_func = hashlib.md5


LOGGER_INST: logging.Logger = logging.getLogger(__file__)
CACHE_PREFIX: str = "hmin-"
MINIFICATION_ENABLED: bool = getattr(settings, "HTML_MINIFY", not settings.DEBUG)
REMOVE_COMMENTS: bool = getattr(settings, "HMIN_REMOVE_COMMENTS", True)
USE_CACHE: bool = getattr(settings, "HMIN_USE_CACHE", True)
TIMEOUT: bool = getattr(settings, "HMIN_CACHE_TIMEOUT", 3600)
EXCLUDE_PAGES: list = []


# get cache provider, or disable caching
if USE_CACHE:
    try:
        cache_instance: BaseCache = caches[getattr(settings, "HMIN_CACHE_BACKEND", "default")]
    except (InvalidCacheBackendError, NameError):
        USE_CACHE = False


# process exclude pages
if hasattr(settings, "HMIN_EXCLUDE"):
    EXCLUDE_PAGES = [re.compile(url_pattern) for url_pattern in settings.HMIN_EXCLUDE]


# Middlewares starts here
class _BasicMiddleware:
    """Basic middleware mixin."""

    def __init__(self, get_response: typing.Callable) -> None:
        self.get_response: typing.Callable = get_response


class MarkMiddleware(_BasicMiddleware):
    """This middleware suposed to be first.

    It mean to be used with cache middlewares in django.
    """

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Allow minification flag."""
        request.need_to_minify = True
        return self.get_response(request)


class MinMiddleware(_BasicMiddleware):
    """Minification middleware itself."""

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Minification goes here."""
        response: HttpResponse = self.get_response(request)

        # prevent from minifying cached pages
        if not MINIFICATION_ENABLED or not hasattr(request, "need_to_minify") or not request.need_to_minify:
            return response

        # prevent from minifying excluded pages
        if EXCLUDE_PAGES:
            current_path: str = request.path.lstrip("/")
            for one_regex in EXCLUDE_PAGES:
                if one_regex.match(current_path):
                    return response

        if "Content-Type" in response and "text/html" in response["Content-Type"]:
            body_content: str = response.content.decode()
            minified_content: str = ""
            if USE_CACHE:
                cache_key: str = f"{CACHE_PREFIX}{hash_func(response.content).hexdigest()}"
                cached_page: typing.Optional[str] = cache_instance.get(cache_key)
                if cached_page:
                    minified_content = cached_page
                else:
                    minified_content = html_minify(body_content, REMOVE_COMMENTS)
                    cache_instance.set(cache_key, minified_content, TIMEOUT)
            else:
                minified_content = html_minify(body_content, REMOVE_COMMENTS)
            response.content = minified_content.encode()
        return response
