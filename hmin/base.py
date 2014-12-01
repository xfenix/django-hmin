# -*- coding: utf-8 -*-
try:
    import re2 as re
except ImportError:
    import re


PLACEHOLDER = '<@!hmin_placeholder_%s_!@>'
RE_REPLACED_TAG = re.compile(
    ur'(<(script|textarea|style|pre).*?>.*?</(script|textarea|style|pre)>)', re.S
)
RE_COMMENTS = re.compile(ur'<!--(?!\[if.*?\]).*?-->', re.S | re.I)
RE_PLACEHOLDER = re.compile(
    ur'%s' % PLACEHOLDER.replace('%s', '([0-9]+)')
)


def minify(content, remove_comments=True):
    # helpers
    def tag_replace(m):
        safe_storage[ m.start()] = m.group(1)
        return PLACEHOLDER %  m.start()

    def tag_return(m):
        return safe_storage[int(m.group(1))]

    # decode unicode
    content = content.decode('UTF-8', 'strict')

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
