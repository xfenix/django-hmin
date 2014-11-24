django-hmin
===========

Django HTML minification middleware (another one, a little bit faster than django-htmlmin)


Installing
==========

For install django-hmin, run on terminal:

    $ pip install django-hmin


Using the midleware
===================

All you need to do is add two middlewares to your ``MIDDLEWARE_CLASSES`` and
enable the ``HTML_MINIFY`` setting:

    MIDDLEWARE_CLASSES = (
        # other middleware classes
        'hmin.middleware.MinMiddleware',
        'hmin.middleware.MarkMiddleware',
    )

Note that if you're using Django's caching middleware, ``MarkMiddleware``
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

##### Excluding

Specify setting:

    EXCLUDE_FROM_MINIFYING = ('^base/', '^admin/')


License
===================
Who cares? Use it whatever you want.
