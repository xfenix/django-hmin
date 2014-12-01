django-hmin
===========

Django HTML minification middleware (another one).
Key feature - speed. Up to 60x time faster, than htmlmin.
Compress html, removes comments, respects (dont remove) conditional comments (IE) by default.


Installing
==========

For install django-hmin, run on terminal:

    $ pip install django-hmin


Extra install options
==========
If you want extraspeed, you can install `re2` (very fast regular expressions) library (`pip install re2` + reqs). Hmin will use it instead of `re`.


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


Using the function
===================

Just import function minify: `from hmin import minify`, than  you can use it with any html you want.
Definition of minify function: `def minify(content, remove_comments=True)`


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


About speed
==========
I try to compress 1mb of html (i think, your usual html is slightly thiner) on my i7 laptop processor and measure time with django-debug-toolbar.

Django overhead took about 40ms (all), this is time without  minification, just plain html, django, etc.

Then i install hmin and htmlmin and just look at the debug toolbar numbers (this is very silly and simple "benchmark"):
- with hmin cpu was about **60ms** (min)
- with htmlmin cpu was about **1200ms** (min)

Minus overhead, plain time: hmin - **20ms**, htmlmin - **1160ms**.

Probably, you can get other numbers. But hmin really faster than  htmlmin.


License
===================
Who cares? Use it whatever you want.
