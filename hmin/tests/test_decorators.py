"""All tests here.
"""
from __future__ import annotations
import codecs
import pathlib

import pytest

from hmin import decorators
from hmin.tests import helpers


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_plain_minify_decorator_with_fixture(test_case: dict[str, str]) -> None:
    """Fixture based test.
    """

    @decorators.minify_plain()
    def _example_function():
        """Example function returns something.
        """
        return test_case["original"]

    assert _example_function() == test_case["min"]


@pytest.mark.parametrize(
    "example_case",
    (
        ("""<div>     """, "<div>"),
        (
            """<div>

            <p>

            """,
            "<div><p>",
        ),
        (
            """<!-- comments by default is removing -->

            yeap
            <div>

            There is no doubt
            </div>
            """,
            "yeap <div> There is no doubt </div>",
        ),
    ),
)
def test_plain_minify_decorator(example_case: str) -> None:
    """Very basic tests.
    """

    @decorators.minify_plain()
    def _example_function():
        """Example function returns something.
        """
        return example_case[0]

    assert _example_function() == example_case[1]
