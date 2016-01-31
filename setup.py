#!/usr/bin/env python

from setuptools import setup

setup(
    name='Vocap',
    version='1.0',
    description='Subtitles indexing tool',
    author='Michal Trunecka',
    author_email='michal.trunecka@gmail.com',
    url='http://www.python.org/sigs/distutils-sig/',
    install_requires=['Django>=1.3','whoosh==2.5.4'],
)
