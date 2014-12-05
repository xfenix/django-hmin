# hi
try:
    from .base import minify
except ImportError:
    from .base2 import minify

__version__='0.3'
