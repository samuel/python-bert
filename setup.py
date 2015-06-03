#!/usr/bin/env python

from distutils.core import setup

__version__ = '2.1.0'

setup(
    name = 'bert',
    version = __version__,
    description = 'BERT Serialization Library',
    author = 'Samuel Stauffer',
    author_email = 'samuel@descolada.com',
    url = 'http://github.com/samuel/python-bert',
    packages = ['bert'],
    install_requires = ["erlastic"],
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
