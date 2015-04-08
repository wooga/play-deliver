"""Setup file for playdeliver."""
from __future__ import print_function
from setuptools import setup, find_packages

import io
import codecs
import os
import sys

import playdeliver

here = os.path.abspath(os.path.dirname(__file__))


def _read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = _read('README.rst', 'CHANGES.rst')

setup(
    name='playdeliver',
    version='1.1.0',
    url='https://github.com/wooga/play-deliver',
    download_url='https://github.com/wooga/play-deliver/archive/1.1.0.tar.gz',
    license='MIT LICENSE',
    author='Manfred Endres',
    install_requires=['docopt==0.6.1',
                      'google-api-python-client==1.4.0',
                      'pycrypto',
                      'pyopenssl'],

    author_email='manfred.endres@wooga.net',
    description='google play store delivering tool',
    long_description=long_description,
    packages=['playdeliver'],
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 2 :: Only',
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Multimedia :: Graphics',
        'Topic :: System :: Archiving :: Packaging',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    scripts=['bin/playdeliver']
)
