# -*- coding: utf-8 -*-

# bla bla, license
from setuptools import setup, find_packages
from hmin import __version__


readme = 'README.md'

try:
    readme = open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), readme
        )
    ).read()
except:
    readme = 'Cool minification middleware for Django'

setup(
    name='django-hmin',
    version=__version__,
    description='html minify middleware for django',
    long_description=readme,
    author='Xfenix',
    author_email='ad@xfenix.ru',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
)
