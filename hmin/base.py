# -*- coding: utf-8 -*-
import re
from django.utils.html import strip_spaces_between_tags


PLACEHOLDER = '<special_%s_safemarker>'
RE_MULTISPACE = re.compile(ur'\s{2,}')
RE_NEWLINE = re.compile(ur'\n')
RE_REPLACED_TAG = re.compile(
    ur'(<(script|textarea|style|pre).*?>.*?</(script|textarea|style|pre)>)', re.S
)
RE_PLACEHOLDER = re.compile(
    ur'%s' % (PLACEHOLDER.replace('%s', '([0-9]+)'))
)


class Minify(object):
    safe_storage = dict()

    def tag_replace(self, match):
        self.safe_storage[match.start()] = match.group(1)
        return PLACEHOLDER % match.start()

    def tag_return(self, match):
        return self.safe_storage[int(match.group(1))]

    def process(self, content):
        content = strip_spaces_between_tags(content.strip())

        # replace real tags with placeholders
        content = RE_REPLACED_TAG.sub(self.tag_replace, content)

        # remove garbadge
        content = RE_MULTISPACE.sub(' ', content)
        content = RE_NEWLINE.sub('', content)

        # return tags instead of placeholders
        return RE_PLACEHOLDER.sub(self.tag_return, content)
