#!/usr/bin/env python

from distutils.core import setup

from bert import __version__ as version

setup(
    name = 'bert',
    version = version,
    description = 'BERT-RPC Library',
    author = 'Samuel Stauffer',
    author_email = 'samuel@lefora.com',
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
