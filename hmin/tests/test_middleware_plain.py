"""All tests here.
"""
from __future__ import annotations
import os
import codecs
import pathlib

import pytest

from hmin import middleware
from hmin.tests import helpers
from hmin.base import html_minify


def test_mark_middleware() -> None:
    """Very simple basic test.
    """
    fake_request: type = type("Empty", (), {})
    middleware_inst: middleware.MarkMiddleware = middleware.MarkMiddleware()
    middleware_inst.process_request(fake_request)
    assert fake_request.need_to_minify


def _run_inner_middleware_test(
    test_case: dict[str, str], need_to_minify: bool = True, content_type: bool = True
) -> None:
    """Inner function.
    """

    class FakeResponse(dict):
        """Fake response class.
        """

        content: str = test_case["original"]

    fake_request: type = type("Empty", (), {"need_to_minify": need_to_minify})
    fake_response: type = FakeResponse()
    if content_type:
        fake_response["Content-Type"] = "text/html"
    middleware_inst: middleware.MinMiddleware = middleware.MinMiddleware()
    middleware_inst.process_response(fake_request, fake_response)
    assert test_case["min" if need_to_minify and content_type else "original"] == fake_response.content


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_min_middleware(test_case: dict[str, str]) -> None:
    """Very simple basic minify test.
    """
    _run_inner_middleware_test(test_case)


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_min_middleware_need_no_minify(test_case: dict[str, str]) -> None:
    """Very simple basic minify test.
    """
    _run_inner_middleware_test(test_case, need_to_minify=False)


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_min_middleware_with_no_content_type(test_case: dict[str, str]) -> None:
    """Very simple basic minify test.
    """
    _run_inner_middleware_test(test_case, content_type=False)


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_min_middleware_with_cache(monkeypatch, test_case: dict[str, str]) -> None:
    """Very simple basic minify test.
    """
    monkeypatch.setattr("django.conf.settings.HMIN_USE_CACHE", False)
    _run_inner_middleware_test(test_case)


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_min_middleware_with_xxhash(test_case: dict[str, str]) -> None:
    """Very simple basic minify test.
    """
    import pip

    pip.main(["install", "xxhash"])
    _run_inner_middleware_test(test_case)
    pip.main(["uninstall", "xxhash"])


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_min_middleware_with_broken_cache(monkeypatch, test_case: dict[str, str]) -> None:
    """Very simple basic minify test.
    """
    monkeypatch.setattr("django.core.cache.caches", {})
    _run_inner_middleware_test(test_case)


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_min_middleware_with_exclude(monkeypatch, test_case: dict[str, str]) -> None:
    """Very simple basic minify test.
    """
    monkeypatch.setattr("django.conf.settings.HMIN_EXCLUDE", ["/", "hello/"])
    _run_inner_middleware_test(test_case)
