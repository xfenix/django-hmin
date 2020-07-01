django-hmin
===========

[![Build Status](https://travis-ci.org/xfenix/django-hmin.svg?branch=master)](https://travis-ci.org/xfenix/django-hmin)
[![PyPI version](https://badge.fury.io/py/django-hmin.svg)](https://badge.fury.io/py/django-hmin)
[![codecov](https://codecov.io/gh/xfenix/django-hmin/branch/master/graph/badge.svg)](https://codecov.io/gh/xfenix/django-hmin)

Django (1.6+) HTML minification middleware (another one).
Key feature - speed. 10x (on large html's it can be 50x, 100x, 200x or even more) time faster, than htmlmin.
Compress html code and removes html comments, but ignores conditional comments (IE) by default.
Uses cache by default (can be disabled), so minification overhead is greatly reduced.


Compatibility
==========
Django 1.6 — Django 1.10


Installing
==========

For install django-hmin, run on terminal:

    $ pip install django-hmin

##### Extra install options
Optionally, you can install `re2` (fast regular expressions) library (`pip install re2` + reqs). Hmin will use it instead of `re`.


Using the midleware
===================

All you need to do is add two middlewares to your ``MIDDLEWARE_CLASSES``:

    MIDDLEWARE_CLASSES = (
        # other middleware classes
        'hmin.middleware.MinMiddleware',
        'hmin.middleware.MarkMiddleware',
    )

If you're using Django's caching middleware, ``MarkMiddleware``
should go after ``FetchFromCacheMiddleware``, and ``MinMiddleware``
should go after ``UpdateCacheMiddleware``:

    MIDDLEWARE_CLASSES = (
      'django.middleware.cache.UpdateCacheMiddleware',
      'hmin.middleware.MinMiddleware',
      # other middleware classes
      'django.middleware.cache.FetchFromCacheMiddleware',
      'hmin.middleware.MarkMiddleware',
    )

You can optionally specify the ``HTML_MINIFY`` setting:

    HTML_MINIFY = True

The default value for the ``HTML_MINIFY`` setting is ``not DEBUG``. You only
need to set it to ``True`` if you want to minify your HTML code when ``DEBUG``
is enabled.

##### URL exclude

Specify setting:

    HMIN_EXCLUDE = ('^base/', '^admin/')

##### Keep html comments

Specify settings:

    HMIN_REMOVE_COMMENTS = False

##### Cache

By default hmin middleware uses cache (very useful for small and middle web sites, and for big you definitely will use ngx_pagespeed or other "big" solutions).
You can disable it by specify setting:

    HMIN_USE_CACHE = False

Also you can change time and cache backend (if you want, by default time is 3600, cache backend - "default"):

    HMIN_CACHE_TIMEOUT = 86400
    HMIN_CACHE_BACKEND = 'my_cache'


Using the function
===================

Just import function minify: `from hmin import minify`, than  you can use it with any html you want.
Function definition: `def minify(content, remove_comments=True)`


Using the decorator
===================

Just import decorator minify_plain: `from hmin.decorators import minify_plain`, than you can minify any function you want:

    @minify_plain()
    def my_cool_func():
        <...>
        return some_plain_html

Or, if you want to keep html comments:

    @minify_plain(False)
    def my_cool_func():
        <...>
        return some_plain_html


Stupid speed benchmark (1)
==========
I try to compress 1mb of html (i think, your usual html is slightly thiner) on my i7 laptop processor and measure time with django-debug-toolbar.

Django overhead took about 40ms (all), this is time without  minification, just plain html, django, etc.

Then i install hmin and htmlmin and just look at the debug toolbar numbers (this is very silly and simple "benchmark"):
- with hmin cpu was about **60ms** (min)
- with htmlmin cpu was about **1200ms** (min)

Minus overhead, plain time: hmin - **20ms**, htmlmin - **1160ms**.

Probably, you can get other numbers. But hmin really faster than  htmlmin.


Stupid speed benchmark (2)
==========
Also i try to compress 2mb of html on my desktop i3 (sandy bridge).

Debug toolbar time:
- with hmin cpu was about **220ms** without cache, and **87ms** with cache
- with htmlmin cpu was about **125000ms**

Django overhead was about **80ms**.
Minus overhead, plain time: hmin - **140ms** (**7ms** with cache), htmlmin - ok.


Current possible problems
===================
- Doesnt respect CDATA
