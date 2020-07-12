"""fake_django URL Configuration.
"""
from django.urls import path

from base import views


urlpatterns = [
    path("", views.IndexView.as_view()),
]
