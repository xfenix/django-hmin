"""For python -m usage."""
import pathlib
import argparse

from hmin.base import html_minify


def main_cli() -> None:
    """Minify CLI functionality."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("filename", type=pathlib.Path)
    parsed_arguments: argparse.Namespace = parser.parse_args()

    parsed_arguments.filename = parsed_arguments.filename.resolve()
    if parsed_arguments.filename.exists() and not parsed_arguments.filename.is_dir():
        print(html_minify(parsed_arguments.filename.read_text()))
    else:
        print("Sorry. Wrong path, cant read data from it!")


main_cli()
