#!/usr/bin/env python
from distutils.core import setup


setup(
    name='pyodnoklassniki',
    version='0.11',
    packages=[
        'pyodnoklassniki',
        'pyodnoklassniki.contrib',
        'pyodnoklassniki.contrib.django',
    ],
    author='Marsel Mavletkulov',
    author_email='marselester@ya.ru',
    url='https://github.com/marselester/pyodnoklassniki/',
    description='Odnoklassniki REST API wrapper.',
    long_description=open('README.rst').read(),
    install_requires=[
        'requests>=1.0',
    ]
)
