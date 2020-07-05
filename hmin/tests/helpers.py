"""Some wide test things.
"""
from __future__ import annotations
import codecs
import pathlib
from collections import defaultdict


DATA_PATH: pathlib.Path = pathlib.Path(__file__).parent.resolve().joinpath("data")
MIN_INFIX: str = "_min"


def load_html_fixtures() -> tuple[dict[str, str]]:
    """Load all html fixtures and return tuple ((original, processed), ...).
    """
    map_key: str
    map_of_files: defaultdict = defaultdict(dict)
    for one_file in DATA_PATH.glob("*.html"):
        map_of_files[one_file.stem.replace(MIN_INFIX, "")][
            "min" if MIN_INFIX in one_file.stem else "original"
        ] = one_file.read_text()
    return map_of_files.values()


# import os
# os.environ["DJANGO_SETTINGS_MODULE"] = "hmin.tests.mock_settings"