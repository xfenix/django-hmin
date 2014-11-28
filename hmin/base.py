# -*- coding: utf-8 -*-
import re


PLACEHOLDER = '[#_idk_%s_lol_#]'
RE_REPLACED_TAG = re.compile(
    ur'(<(script|textarea|style|pre).*?>.*?</(script|textarea|style|pre)>)', re.S
)
RE_COMMENTS = re.compile(ur'<!--.*?-->', re.S)
RE_PLACEHOLDER = re.compile(
    ur'%s' % (PLACEHOLDER.replace('%s', '([0-9]+)'))
)


def minify(content, remove_comments=True):
    # helpers
    tag_replace = lambda m: safe_storage[m.start()] = m.group(1);\
                            PLACEHOLDER % m.start()
    tag_return = lambda m: safe_storage[int(m.group(1))]
    safe_storage = dict()

    # decode unicode
    try:
        content = content.decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        pass

    # replace dangerous tags with placeholders
    content = RE_REPLACED_TAG.sub(tag_replace, content)

    # remove garbadge (spaces, comments, newlines)
    content = ' '.join(content.split())
    content = content.replace('> <', '><')
    if remove_comments:
        content = RE_COMMENTS.sub('', content)

    # return tags instead of placeholders
    return RE_PLACEHOLDER.sub(tag_return, content)
