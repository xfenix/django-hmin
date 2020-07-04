"""Django middleware.
"""
from __future__ import annotations
import re
import typing
import logging

from django.conf import settings
from django.core.caches.backends.base import BaseCache
from django.core.cache import caches, InvalidCacheBackendError

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
try:
    cache_instance: BaseCache = caches[getattr(settings, "HMIN_CACHE_BACKEND", "default")]
except (InvalidCacheBackendError, NameError):
    USE_CACHE = False


# process exclude pages
if hasattr(settings, "HMIN_EXCLUDE"):
    EXCLUDE_PAGES = [re.compile(url_pattern) for url_pattern in settings.HMIN_EXCLUDE]


# Middlewares starts here
class MarkMiddleware:
    """This middleware suposed to be first. It mean to be used with cache middlewares in django.
    """

    def process_request(self, request):
        """Allow minification flag.
        """
        request.need_to_minify = True


class MinMiddleware:
    """Minification middleware itself.
    """

    def process_response(self, request, response):
        """Minification goes here.
        """
        # prevent from minifying cached pages
        if not hasattr(request, "need_to_minify") or not request.need_to_minify:
            return response

        # prevent from minifying excluded pages
        if EXCLUDE_PAGES:
            current_path: str = request.path.lstrip("/")
            for one_regex in EXCLUDE_PAGES:
                if one_regex.match(current_path):
                    return response

        if "Content-Type" in response and "text/html" in response["Content-Type"] and MINIFICATION_ENABLED:
            if USE_CACHE:
                cache_key: str = f"{CACHE_PREFIX}{hash_func(response.content).hexdigest()}"
                cached_page: typing.Optional[str] = cache_instance.get(cache_key)
                if cached_page:
                    response.content = cached_page
                else:
                    response.content = html_minify(response.content, REMOVE_COMMENTS)
                    cache_instance.set(cache_key, response.content, TIMEOUT)
            else:
                response.content = html_minify(response.content, REMOVE_COMMENTS)
        return response
