"""All tests here."""
from __future__ import annotations
import os
import codecs
import pathlib
import importlib
from unittest import mock

import pip
import pytest

from hmin import middleware
from hmin.tests import helpers
from hmin.base import html_minify


def test_mark_middleware() -> None:
    """Very simple basic test."""
    fake_request: type = type("Empty", (), {})
    middleware.MarkMiddleware(lambda _: None)(fake_request)
    assert fake_request.need_to_minify


def _run_inner_middleware_test(
    test_case: dict[str, str], need_to_minify: bool = True, content_type: bool = True, compare_min: bool = True
) -> None:
    """Inner function."""

    class FakeResponse(dict):
        """Fake response class."""

        content: bytes = test_case["original"].encode()

    fake_request: type = type("Empty", (), {"need_to_minify": need_to_minify, "path": "debug"})
    fake_response: type = FakeResponse()
    if content_type:
        fake_response["Content-Type"] = "text/html"
    middleware_inst: middleware.MinMiddleware = middleware.MinMiddleware(lambda _: fake_response)
    middleware_inst(fake_request)
    assert test_case["min" if compare_min else "original"] == fake_response.content.decode()


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_min_middleware(test_case: dict[str, str]) -> None:
    """Very simple basic minify test."""
    _run_inner_middleware_test(test_case)


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_min_middleware_need_no_minify(test_case: dict[str, str]) -> None:
    """Very simple basic minify test."""
    _run_inner_middleware_test(test_case, need_to_minify=False, compare_min=False)


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_min_middleware_with_no_content_type(test_case: dict[str, str]) -> None:
    """Very simple basic minify test."""
    _run_inner_middleware_test(test_case, content_type=False, compare_min=False)


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_min_middleware_with_cache(monkeypatch, test_case: dict[str, str]) -> None:
    """Very simple basic minify test."""
    _run_inner_middleware_test(test_case)


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_min_middleware_without_xxhash(monkeypatch, test_case: dict[str, str]) -> None:
    """Very simple basic minify test."""
    pip.main(["uninstall", "xxhash"])
    importlib.reload(middleware)
    _run_inner_middleware_test(test_case)


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_min_middleware_with_xxhash(monkeypatch, test_case: dict[str, str]) -> None:
    """Very simple basic minify test."""
    pip.main(["install", "xxhash"])
    importlib.reload(middleware)
    _run_inner_middleware_test(test_case)
    pip.main(["uninstall", "xxhash"])


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_min_middleware_with_broken_cache(monkeypatch, settings, test_case: dict[str, str]) -> None:
    """Very simple basic minify test."""
    settings.HMIN_USE_CACHE = False
    importlib.reload(middleware)
    _run_inner_middleware_test(test_case)


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_min_middleware_with_exclude(monkeypatch, test_case: dict[str, str], settings) -> None:
    """Very simple basic minify test."""
    settings.HMIN_EXCLUDE = ["hello/", "unrelated/", "strange/trash/happens/"]
    importlib.reload(middleware)
    _run_inner_middleware_test(test_case)


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_min_middleware_with_exclude_really(monkeypatch, test_case: dict[str, str], settings) -> None:
    """Very simple basic minify test."""
    settings.HMIN_EXCLUDE = [
        "debug",
    ]
    importlib.reload(middleware)
    _run_inner_middleware_test(test_case, compare_min=False)


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_bad_caches(monkeypatch, test_case: dict[str, str], settings) -> None:
    """Very simple basic minify test."""

    class FakeDict:
        """Raise exception for caches fetching."""

        def __getitem__(self, _) -> None:
            """Obvious."""
            raise NameError

    monkeypatch.setattr("django.core.cache.caches", FakeDict())
    importlib.reload(middleware)
    _run_inner_middleware_test(test_case, compare_min=True)
