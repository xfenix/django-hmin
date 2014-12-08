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


# post install hook
class InstallWrapper(install):
    def run(self):
        install.run(self)
        mod_path = os.path.dirname(self.get_outputs()[0])
        os.chdir(os.path.join(os.getcwd(), 'hmin_cpp'))
        print call(['sh', 'build.sh'])


setup(
    name='django-hmin',
    version=__version__,
    description=descr,
    long_description=readme,
    author='Xfenix',
    author_email='ad@xfenix.ru',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    #cmdclass={'install': InstallWrapper}
)
