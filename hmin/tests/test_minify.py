"""All tests here.
"""
import codecs
import pathlib

from django.test import SimpleTestCase
from django.test.utils import override_settings

from hmin import minify


DATA_PATH: pathlib.Path = pathlib.Path(__file__).parent.resolve().joinpath("data")


def load_fixture_file(file_name: str) -> str:
    """Test helper fn.
    """
    return codecs.open("%s.html" % DATA_PATH.joinpath(file_name), encoding="utf-8").read()


class MinifyTestCase(SimpleTestCase):
    """Basic test case.
    """

    def test_with_fixture_data(self):
        """Fixture based test.
        """
        examples = [
            "habrahabr",
            "lenta",
            "gazeta",
            "youtube",
        ]
        for one_example in examples:
            print("Test file %s" % one_example)
            self.assertEqual(minify(load_fixture_file(one_example)), load_fixture_file(one_example + "_min"))
