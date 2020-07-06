"""Core logic module.
"""
from __future__ import annotations
import re
import logging


LOGGER_INST: logging.Logger = logging.getLogger(__file__)
RE_FLAGS: re.RegexFlag = re.S | re.I
PLACEHOLDER: str = "<@!hmin_placeholder_%s_!@>"
RE_SAFE_EXCLUDE_TAGS_RE: re.Pattern = re.compile(
    r"(<(script|textarea|style|pre).*?>.*?</(script|textarea|style|pre)>)", flags=RE_FLAGS
)
RE_COMMENTS: re.Pattern = re.compile(r"<!--(?!\[if.*?\]).*?-->", flags=RE_FLAGS)
RE_PLACEHOLDER: re.Pattern = re.compile(r"%s" % PLACEHOLDER.replace("%s", "([0-9]+)"))
RE_LEFT_SPACES_AROUND_TAGS: re.Pattern = re.compile(r"(?:\s|)(<.*?>)(?:\s|)", flags=re.S | re.I | re.U)


def html_minify(data_input: str, remove_comments=True) -> str:
    """Core minification function.
    """
    safe_storage: dict = dict()

    # helpers
    def store_excluded_tags(match: re.Match) -> str:
        safe_storage[match.start()] = match.group(1)
        return PLACEHOLDER % match.start()

    def return_excluded_tags(match: re.Match) -> str:
        return safe_storage[int(match.group(1))]

    # replace dangerous tags with placeholders
    data_input = RE_SAFE_EXCLUDE_TAGS_RE.sub(store_excluded_tags, data_input)
    # fast version of "\s{2,} to \s"
    data_input = " ".join(data_input.split())
    # "strip_space_between_tags"
    data_input = data_input.replace("> <", "><")
    data_input = RE_LEFT_SPACES_AROUND_TAGS.sub(r"\1", data_input)
    if remove_comments:
        data_input = RE_COMMENTS.sub("", data_input)

    # and return dangerous tags back
    return RE_PLACEHOLDER.sub(return_excluded_tags, data_input).strip()
