"""Some inter tests things."""
from django.conf import settings


def pytest_configure() -> None:
    """Django config."""
    settings.configure(
        DEBUG=True,
        SECRET_KEY="no",
        DATABASES={},
        HTML_MINIFY=True,
        HMIN_USE_CACHE=True,  # HMIN_EXCLUDE=["/", "hello/"],
    )
