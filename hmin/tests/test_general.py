"""All tests here.
"""
from __future__ import annotations
import pathlib
import runpy

import pytest

from hmin.tests import helpers


def test_main(monkeypatch):
    """Check -m command.
    """
    full_main_fpath: str = str(pathlib.Path(__file__).parent.parent.resolve().joinpath("__main__.py"))
    monkeypatch.setattr("sys.argv", [full_main_fpath, str(helpers.DATA_PATH.joinpath("gazeta.html"))])
    runpy.run_path(full_main_fpath)
