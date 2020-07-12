"""Django settings for fake_django project.
"""
import os
import pathlib


BASE_DIR = pathlib.Path(__file__).parent
SECRET_KEY = "razwx%pkjekemw^r^0tzhd^d4!8vlj*3@j9lh_=rc(p)br%m+j"
DEBUG = True
ALLOWED_HOSTS = []
WSGI_APPLICATION = "fake_django.wsgi.application"
ROOT_URLCONF = "fake_django.urls"
STATIC_URL = "/static/"

HTML_MINIFY = True
HMIN_USE_CACHE = False

# Application definition
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "base",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # other middleware classes
    "hmin.middleware.MinMiddleware",
    "hmin.middleware.MarkMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
