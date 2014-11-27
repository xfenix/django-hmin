# -*- coding: utf-8 -*-
from django.conf import settings

from base import Minify


""" Minification html middleware
"""
ENABLED = getattr(settings, 'HTML_MINIFY', not settings.DEBUG)
EXCLUDE = []
minifier = Minify()


if hasattr(settings, 'EXCLUDE_FROM_MINIFYING'):
    for url_pattern in settings.EXCLUDE_FROM_MINIFYING:
        regex = re.compile(url_pattern)
        EXCLUDE.append(regex)


class MarkMiddleware(object):
    def process_request(self, request):
        request.need_to_minify = True


class MinMiddleware(object):
    def process_response(self, request, response):
        # prevent from minifying cached pages
        if not hasattr(request, 'need_to_minify'):
            return response

        # prevent from minifying excluded pages
        path = request.path.lstrip('/')
        for regex in EXCLUDE:
            if regex.match(path):
                return response

        if 'Content-Type' in response and\
           'text/html' in response['Content-Type'] and ENABLED:
            response.content = minifier.process(response.content)
        return response
