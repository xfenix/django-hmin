"""Mock settings for django.
"""
from __future__ import annotations


DEBUG: bool = True
SECRET_KEY: str = "no"
DATABASES: dict = {}
HTML_MINIFY: bool = True
HMIN_USE_CACHE: bool = True
HMIN_EXCLUDE: list = []
