from distutils.core import setup, Extension


setup (
    name = 'minify function',
    version = '0.3',
    description = 'This is a min package',
    ext_modules = [
        Extension('base', sources = ['base.c']),
    ]
)
