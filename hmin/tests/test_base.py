"""All tests here.
"""
from __future__ import annotations
import codecs
import pathlib

import pytest

from hmin import minify
from hmin.tests.conftest import load_fixture_file


@pytest.mark.parametrize("fixture_file_name", ("habrahabr", "lenta", "gazeta", "youtube"))
def test_with_fixture_data(fixture_file_name: str) -> None:
    """Fixture based test.
    """
    print("Test file %s" % fixture_file_name)
    assert minify(load_fixture_file(fixture_file_name)) == load_fixture_file(fixture_file_name + "_min")


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
def test_some_basic_things(example_case: str) -> None:
    """Very basic tests.
    """
    assert minify(example_case[0]) == example_case[1]
