# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from hmin import __version__


readme = 'README.md'

try:
    import pypandoc
    read = lambda: pypandoc.convert(readme, 'rst')
except:
    readme = open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), readme
        )
    ).read()


setup(
    name='django-hmin',
    version=__version__,
    description='HTML minification function, django middleware, decorator',
    long_description=readme,
    author='Xfenix',
    author_email='ad@xfenix.ru',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
)
