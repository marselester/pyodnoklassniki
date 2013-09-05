#!/usr/bin/env python
from distutils.core import setup


setup(
    name='pyodnoklassniki',
    version='0.1',
    packages=['pyodnoklassniki'],
    author='Marsel Mavletkulov',
    author_email='marselester@ya.ru',
    url='https://github.com/marselester/pyodnoklassniki/',
    description='Odnoklassniki REST API wrapper.',
    long_description=open('README.rst').read(),
    install_requires=[
        'requests>=1.0',
    ]
)