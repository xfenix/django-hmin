# -*- coding: utf-8 -*-
import os
from django.conf import settings

# try:
#     from .base import minify
# except ImportError:
#     from .base2 import minify

# hello, dirty hack
old_folder = os.getcwd()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from jnius import autoclass
os.chdir(old_folder)


""" Minification html middleware
"""
ENABLED = getattr(settings, 'HTML_MINIFY', not settings.DEBUG)
REMOVE_COMMENTS = getattr(settings, 'HMIN_REMOVE_COMMENTS', True)
EXCLUDE = []

# get minifier
minify = autoclass('Minify')
java_remove_comments = autoclass('java.lang.Boolean')(REMOVE_COMMENTS)


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
            pass#response.content = minify.compress(response.content)
        return response
