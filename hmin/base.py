# -*- coding: utf-8 -*-
from __future__ import unicode_literals
try:
    import re2 as re
except ImportError:
    import re

flags = re.S | re.I
PLACEHOLDER = '<@!hmin_placeholder_%s_!@>'
RE_REPLACED_TAG = re.compile(
    r'(<(script|textarea|style|pre).*?>.*?</(script|textarea|style|pre)>)',
    flags
)
RE_COMMENTS = re.compile(r'<!--(?!\[if.*?\]).*?-->', flags)
RE_PLACEHOLDER = re.compile(
    r'%s' % PLACEHOLDER.replace('%s', '([0-9]+)')
)


def minify(content, remove_comments=True):
    # helpers
    def tag_replace(m):
        safe_storage[m.start()] = m.group(1)
        return PLACEHOLDER %  m.start()

    def tag_return(m):
        return safe_storage[int(m.group(1))]

    # decode unicode
    try:
        content = content.decode('utf8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        pass

    # replace dangerous tags with placeholders
    safe_storage = dict()
    content = RE_REPLACED_TAG.sub(tag_replace, content)

    # fast version of "\s{2,} to \s"
    content = ' '.join(content.split())
    # "strip_space_between_tags"
    content = content.replace('> <', '><')
    if remove_comments:
        content = RE_COMMENTS.sub('', content)

    # and return dangerous tags back
    return RE_PLACEHOLDER.sub(tag_return, content).strip()
