"""All tests here.
"""
from __future__ import annotations
import codecs
import pathlib

import pytest

from hmin import decorators
from hmin.tests.conftest import load_fixture_file


@pytest.mark.parametrize("fixture_file_name", ("habrahabr", "lenta", "gazeta", "youtube"))
def test_plain_minify_decorator_with_fixture(fixture_file_name: str) -> None:
    """Fixture based test.
    """
    print("Test file %s" % fixture_file_name)

    @decorators.minify_plain()
    def _example_function():
        """Example function returns something.
        """
        return load_fixture_file(fixture_file_name)

    assert _example_function() == load_fixture_file(fixture_file_name + "_min")


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
