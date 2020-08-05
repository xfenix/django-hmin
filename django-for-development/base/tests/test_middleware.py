"""Test django integration."""
from django.test import Client
from django.http import HttpResponse


def test_middleware_indexpage():
    """Test."""
    view_response: HttpResponse = Client().get("/")
    assert (
        view_response.content
        == b'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Document</title></head><body>This is test</body></html>'
    )
