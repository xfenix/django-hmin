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


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_min_middleware(test_case: dict[str, str]) -> None:
    """Very simple basic minify test.
    """

    class FakeResponse(dict):
        """Fake response class.
        """

        content: str = test_case["original"]

    fake_request: type = type("Empty", (), {"need_to_minify": True})
    fake_response: type = FakeResponse()
    fake_response["Content-Type"] = "text/html"
    middleware_inst: middleware.MinMiddleware = middleware.MinMiddleware()
    middleware_inst.process_response(fake_request, fake_response)
    assert test_case["min"] == fake_response.content


@pytest.mark.parametrize("test_case", helpers.load_html_fixtures())
def test_min_middleware_with_cache(monkeypatch, test_case: dict[str, str]) -> None:
    """Very simple basic minify test.
    """
    from django.conf import settings

    class FakeResponse(dict):
        """Fake response class.
        """

        content: str = test_case["original"]

    fake_request: type = type("Empty", (), {"need_to_minify": True})
    fake_response: type = FakeResponse()
    fake_response["Content-Type"] = "text/html"
    settings.HMIN_USE_CACHE = False
    monkeypatch.setattr("django.conf.settings", settings)
    middleware_inst: middleware.MinMiddleware = middleware.MinMiddleware()
    middleware_inst.process_response(fake_request, fake_response)
    assert test_case["min"] == fake_response.content
