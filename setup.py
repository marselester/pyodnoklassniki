#!/usr/bin/env python
from setuptools import setup

setup(
    name='pyodnoklassniki',
    version='1.0.0',
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
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ]
)
