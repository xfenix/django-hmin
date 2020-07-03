"""Some wide test things.
"""
import codecs
import pathlib


DATA_PATH: pathlib.Path = pathlib.Path(__file__).parent.resolve().joinpath("data")


def load_fixture_file(file_name: str) -> str:
    """Test helper fn.
    """
    return codecs.open("%s.html" % DATA_PATH.joinpath(file_name), encoding="utf-8").read()


# import os
# os.environ["DJANGO_SETTINGS_MODULE"] = "hmin.tests.mock_settings"
