"""Some wide test things."""
from __future__ import annotations
import codecs
import pathlib
from collections import defaultdict


TESTS_PATH: pathlib.Path = pathlib.Path(__file__).parent.resolve()
ROOT_PATH: pathlib.Path = TESTS_PATH.parent.resolve()
DATA_PATH: pathlib.Path = TESTS_PATH.resolve().joinpath("data")
MIN_INFIX: str = "_min"
TYPICAL_HTML_CASES: tuple = (
    ("""<div>     """, "<div>"),
    (
        """<div data-kek=\"500\">  hey    
            <p> <!-- trash -->
            """,
        '<div data-kek="500">hey <p>',
    ),
    (
        """<!-- comments by default is removing -->


            yeap
            <div>

            <a href="#"> There is no doubt   </a>
            </div>
            """,
        'yeap <div><a href="#">There is no doubt</a></div>',
    ),
    (
        """
            <a href="#">
            asdsad
            </a>
            """,
        '<a href="#">asdsad</a>',
    ),
    (
        """<div style="border: 1px solid grey; color: green"><p><br>

        Broken HTML?</ >
            """,
        '<div style="border: 1px solid grey; color: green"><p><br>Broken HTML?</ >',
    ),
    ("privet    >   1000    <           kak", "privet > 1000 < kak",),
    ("         ", ""),
    ("<div> </div>", "<div></div>"),
    ('<b> hm <a href="#">what</a> </b>', '<b>hm <a href="#">what</a></b>'),
    ('<span>          good text   </span>  for all people', '<span>good text</span> for all people'),
)


def load_html_fixtures() -> tuple[dict[str, str]]:
    """Load all html fixtures and return tuple ((original, processed), ...)."""
    map_key: str
    map_of_files: defaultdict = defaultdict(dict)
    for one_file in DATA_PATH.glob("*.html"):
        map_of_files[one_file.stem.replace(MIN_INFIX, "")][
            "min" if MIN_INFIX in one_file.stem else "original"
        ] = one_file.read_text().strip()
    return tuple(map_of_files.values())
