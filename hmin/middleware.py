# -*- coding: utf-8 -*-
import re
from django.utils.html import strip_spaces_between_tags
from django.conf import settings


""" Minification html middleware

reduce client-side traffic
"""
PLACEHOLDER = '<special_%s_safemarker>'
RE_MULTISPACE = re.compile(ur'\s{2,}')
RE_NEWLINE = re.compile(ur'\n')
RE_REPLACED_TAG = re.compile(
    ur'(<(script|textarea|pre).*?>.*?</(script|textarea|pre)>)', re.S
)
RE_PLACEHOLDER = re.compile(
    ur'%s' % (PLACEHOLDER.replace('%s', '([0-9]+)'))
)
ENABLED = getattr(settings, 'HTML_MINIFY', not settings.DEBUG)
EXCLUDE = []

if hasattr(settings, 'EXCLUDE_FROM_MINIFYING'):
    for url_pattern in settings.EXCLUDE_FROM_MINIFYING:
        regex = re.compile(url_pattern)
        EXCLUDE.append(regex)


class MarkMiddleware(object):
    def process_request(self, request):
        request.need_to_minify = True


class MinMiddleware(object):
    def tag_replace(self, match):
        self.safe_storage[match.start()] = match.group(1)
        return PLACEHOLDER % match.start()

    def tag_return(self, match):
        return self.safe_storage[int(match.group(1))]

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
            response.content = strip_spaces_between_tags(
                response.content.strip()
            )

            self.safe_storage = dict()

            # replace real tags with placeholders
            response.content = RE_REPLACED_TAG.sub(
                self.tag_replace, response.content
            )

            # remove garbadge
            response.content = RE_MULTISPACE.sub(' ', response.content)
            response.content = RE_NEWLINE.sub('', response.content)

            # return tags instead of placeholders
            response.content = RE_PLACEHOLDER.sub(
                self.tag_return, response.content
            )
        return response
