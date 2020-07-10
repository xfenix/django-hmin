django-hmin
===

![Build and publish](https://github.com/xfenix/django-hmin/workflows/Build%20and%20publish/badge.svg)
[![PyPI version](https://badge.fury.io/py/django-hmin.svg)](https://badge.fury.io/py/django-hmin)
[![codecov](https://codecov.io/gh/xfenix/django-hmin/branch/master/graph/badge.svg)](https://codecov.io/gh/xfenix/django-hmin)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

Django (2.0+) oriented HTML minification function and middleware (another one).  
Key feature — speed. 10x (on large html's it can be 50x, 100x, 200x or even more) time faster, than htmlmin.

Compress html code and removes html comments, but ignores conditional comments (IE) by default.  
Uses cache by default (can be disabled), so minification overhead is greatly reduced.  
Also it can be used as solo function.  
For best expirience use it with https://github.com/django-compressor/django-compressor.

Written in modern python 3.7+ with fully typing-covered codebase.

Full support of:
* https://www.python.org/dev/peps/pep-0526/
* https://www.python.org/dev/peps/pep-0484/
* https://www.python.org/dev/peps/pep-0008/
* https://www.python.org/dev/peps/pep-0257/


Compatibility
===
* Python 3.7+
* Django 2.0+ (not required)


Install
===
For install django-hmin, run on terminal:
```bash
$ pip install django-hmin
```

Using with Django as midleware
===

All you need to do is add two middlewares to your ``MIDDLEWARE_CLASSES``:
```python
MIDDLEWARE_CLASSES: tuple = (
    # other middleware classes
    'hmin.middleware.MinMiddleware',
    'hmin.middleware.MarkMiddleware',
)
```

If you're using Django's caching middleware, ``MarkMiddleware``
should go after ``FetchFromCacheMiddleware``, and ``MinMiddleware``
should go after ``UpdateCacheMiddleware``:
```python
MIDDLEWARE_CLASSES: tuple = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'hmin.middleware.MinMiddleware',
    # other middleware classes
    'django.middleware.cache.FetchFromCacheMiddleware',
    'hmin.middleware.MarkMiddleware',
)
```

You can optionally specify the ``HTML_MINIFY`` setting:
```python
HTML_MINIFY: bool = True
```

The default value for the ``HTML_MINIFY`` setting is ``not DEBUG``. You only
need to set it to ``True`` if you want to minify your HTML code when ``DEBUG``
is enabled.

##### URL exclude
Specify setting:
```python
HMIN_EXCLUDE: tuple = ('^base/', '^admin/')
```

##### Keep HTML comments
Specify settings:
```python
HMIN_REMOVE_COMMENTS: bool = False
```

##### Cache
By default hmin middleware uses cache via django caches framework (very useful for small and middle web sites, and for big you definitely will use ngx_pagespeed or other "big" solutions).
You can disable it by specify setting:
```python
HMIN_USE_CACHE: bool = False
```

Also you can change time and cache backend (if you want, by default time is 3600, cache backend — "default"):
```python
HMIN_CACHE_TIMEOUT: int = 86400
HMIN_CACHE_BACKEND: str = 'my_cache'
```

Another using scenarios
===
## Decorators
Just import decorator minify_plain: `from hmin.decorators import minify_plain`, than you can minify any function you want:
```python
@minify_plain()
def my_cool_func():
    <...>
    return some_plain_html
```

Or, if you want to keep html comments:
```python
@minify_plain(False)
def my_cool_func():
    <...>
    return some_plain_html
```


## Solo
Just import function minify. Function definition: `def minify(content, remove_comments=True)`. Example:
```python
from hmin import html_minify


html_minify('<div>     hello</div>') # <div>hello</div>
```


## CLI
```bash
$ python -m hmin filename.html > filename.min.html
```


Benchmarking (wannabe)
==
## Stupid speed benchmark (1)
I try to compress 1mb of html (i think, your usual html is slightly thiner) on my i7 laptop processor and measure time with django-debug-toolbar.

Django overhead took about 40ms (all), this is time without  minification, just plain html, django, etc.

Then i install hmin and htmlmin and just look at the debug toolbar numbers (this is very silly and simple "benchmark"):
- with hmin cpu was about **60ms** (min)
- with htmlmin cpu was about **1200ms** (min)

Minus overhead, plain time: hmin - **20ms**, htmlmin - **1160ms**.

Probably, you can get other numbers. But hmin really faster than  htmlmin.


## Stupid speed benchmark (2)
Also i try to compress 2mb of html on my desktop i3 (sandy bridge).

Debug toolbar time:
- with hmin cpu was about **220ms** without cache, and **87ms** with cache
- with htmlmin cpu was about **125000ms**

Django overhead was about **80ms**.
Minus overhead, plain time: hmin - **140ms** (**7ms** with cache), htmlmin - ok.


Current possible problems
==
* Doesnt respect CDATA
