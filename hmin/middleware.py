# -*- coding: utf-8 -*-
from django.conf import settings
try:
    from django.core.cache import caches, InvalidCacheBackendError
except ImportError:
    from django.core.cache import get_cache, InvalidCacheBackendError
try:
    import xxhash
    hash_func = xxhash.xxh64
except ImportError:
    import hashlib
    hash_func = hashlib.md5
try:
    import re2 as re
except ImportError:
    import re
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    # Not required for Django <= 1.9, see:
    # https://docs.djangoproject.com/en/1.10/topics/http/middleware/#upgrading-pre-django-1-10-style-middleware
    MiddlewareMixin = object
from .base import minify


""" Minification html middleware
"""
ENABLED = getattr(settings, 'HTML_MINIFY', not settings.DEBUG)
REMOVE_COMMENTS = getattr(settings, 'HMIN_REMOVE_COMMENTS', True)
USE_CACHE = getattr(settings, 'HMIN_USE_CACHE', True)
TIMEOUT = getattr(settings, 'HMIN_CACHE_TIMEOUT', 3600)
EXCLUDE = []

# get cache provider, or disable caching
cache_back = getattr(settings, 'HMIN_CACHE_BACKEND', 'default')
try:
    try:
        cache = caches[cache_back]
    except NameError:
        cache = get_cache(cache_back)
except InvalidCacheBackendError:
    USE_CACHE = False


# process exclude pages
if hasattr(settings, 'HMIN_EXCLUDE'):
    for url_pattern in settings.HMIN_EXCLUDE:
        regex = re.compile(url_pattern)
        EXCLUDE.append(regex)


class MarkMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.need_to_minify = True


class MinMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # prevent from minifying cached pages
        if not hasattr(request, 'need_to_minify') or\
           not request.need_to_minify:
            return response

        # prevent from minifying excluded pages
        if EXCLUDE:
            path = request.path.lstrip('/')
            for regex in EXCLUDE:
                if regex.match(path):
                    return response

        if 'Content-Type' in response and\
                'text/html' in response['Content-Type'] and ENABLED:
            if USE_CACHE:
                key = 'hmin_%s' % hash_func(response.content).hexdigest()
                data = cache.get(key)
                if data:
                    response.content = data
                else:
                    response.content = minify(response.content, REMOVE_COMMENTS)
                    cache.set(key, response.content, TIMEOUT)
            else:
                response.content = minify(response.content, REMOVE_COMMENTS)
        return response
