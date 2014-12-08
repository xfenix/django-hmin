# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.cache import caches, InvalidCacheBackendError
import xxhash

from .base import minify


""" Minification html middleware
"""
ENABLED = getattr(settings, 'HTML_MINIFY', not settings.DEBUG)
REMOVE_COMMENTS = getattr(settings, 'HMIN_REMOVE_COMMENTS', True)
USE_CACHE = getattr(settings, 'HMIN_USE_CACHE', True)
TIMEOUT = getattr(settings, 'HMIN_CACHE_TIMEOUT', 60*60)
EXCLUDE = []

try:
    cache = caches[getattr(settings, 'HMIN_CACHE_BACKEND', 'default')]
except InvalidCacheBackendError:
    USE_CACHE = False

if hasattr(settings, 'HMIN_EXCLUDE'):
    for url_pattern in settings.HMIN_EXCLUDE:
        regex = re.compile(url_pattern)
        EXCLUDE.append(regex)


class MarkMiddleware(object):
    def process_request(self, request):
        request.need_to_minify = True


class MinMiddleware(object):
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
                key = 'hmin_%s' % xxhash.xxh64(response.content).hexdigest()
                data = cache.get(key)
                if data:
                    response.content = data
                else:
                    response.content = minify(response.content, REMOVE_COMMENTS)
                    cache.set(key, response.content, TIMEOUT)
            else:
                response.content = minify(response.content, REMOVE_COMMENTS)
        return response
