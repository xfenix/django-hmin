# -*- coding: utf-8 -*-

# bla bla, license
from setuptools import setup, find_packages
from hmin import __version__


try:
    readme = open('README.md').read()
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
