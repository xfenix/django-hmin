"""All tests here."""
from __future__ import annotations
import codecs
import pathlib

import pytest

from hmin import decorators
from hmin.tests import helpers


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_plain_minify_decorator_with_fixture(test_case: dict[str, str]) -> None:
    """Fixture based test."""

    @decorators.minify_plain()
    def _example_function():
        """Example function returns something."""
        return test_case["original"]

    assert _example_function() == test_case["min"]


@pytest.mark.parametrize("example_case", helpers.TYPICAL_HTML_CASES)
def test_plain_minify_decorator(example_case: str) -> None:
    """Very basic tests."""

    @decorators.minify_plain()
    def _example_function():
        """Example function returns something."""
        return example_case[0]

    assert _example_function() == example_case[1]


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_minify_disable_decorator_with_fixture(test_case: dict[str, str]) -> None:
    """Fixture based test."""

    @decorators.minify_disable
    def _example_function():
        """Example function returns something."""
        fake_response: type = type("Empty", (), {})
        fake_response.data = test_case["original"]
        return fake_response

    _result: typing.Any = _example_function()
    assert _result.data == test_case["original"]
    assert not _result.need_to_minify
