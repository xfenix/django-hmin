# -*- coding: utf-8 -*-
import os
from subprocess import call
from setuptools import setup, find_packages
from setuptools.command.install import install
from hmin import __version__


# readme
descr = 'HTML minification function, django middleware, decorator'

try:
    readme = open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'README.md'
        )
    ).read()
except IOError:
    readme = descr

try:
    import pypandoc
    readme = pypandoc.convert(readme, 'rst', format='md')
except:
    pass


setup(
    name='django-hmin',
    version=__version__,
    description=descr,
    long_description=readme,
    author='Xfenix',
    author_email='ad@xfenix.ru',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[]
)
