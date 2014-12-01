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


def minify(content, remove_comments=True):
    # helpers
    def tag_replace(m):
        key = PLACEHOLDER % m.start()
        safe_storage[key] = m.group(1)
        return key

    # decode unicode
    try:
        content = content.decode('utf-8')
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
    for key, value in safe_storage.items():
        content = content.replace(key, value)

    return content
