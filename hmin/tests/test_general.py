"""All tests here."""
from __future__ import annotations
import pathlib
import runpy

import pytest

from hmin.tests import helpers


@pytest.mark.parametrize("fail_case", (True, False))
def test_main(monkeypatch, fail_case: bool) -> None:
    """Check -m command."""
    full_main_fpath: str = str(helpers.ROOT_PATH.joinpath("__main__.py"))
    monkeypatch.setattr(
        "sys.argv",
        [
            full_main_fpath,
            "non_existen.HAHAHA.LOL.bin" if fail_case else str(helpers.DATA_PATH.joinpath("gazeta.html")),
        ],
    )
    runpy.run_path(full_main_fpath)
