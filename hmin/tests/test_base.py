"""All tests here."""
from __future__ import annotations
import codecs
import pathlib

import pytest

from hmin import html_minify
from hmin.tests import helpers


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_with_fixture_data(test_case: dict[str, str]) -> None:
    """Fixture based test."""
    assert html_minify(test_case["original"]) == test_case["min"], "Wrong case"


@pytest.mark.parametrize("example_case", helpers.TYPICAL_HTML_CASES)
def test_some_basic_things(example_case: str) -> None:
    """Very basic tests."""
    assert html_minify(example_case[0]) == example_case[1]
