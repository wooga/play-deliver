play-deliver
============

Upload screenshots, metadata of your app to the Play Store using a
single command

deliver can upload app screenshots google play backend.

usage
-----

::

    """playdeliver

    Usage:
        playdeliver [options] upload <package-name> <output_dir>
        playdeliver [options] init <package-name> <output_dir>
        playdeliver (-h | --help)
        playdeliver --version

    Options:
      -h --help                 Show this screen.
      --version                 Show version.
      --service-email=<e>       Account service email
      --key=<k>                 Path to *.p12 keyfile
    """

requirements
------------

-  OSX (did not test on linux or windows)
-  python 2.7
-  a play service user for you game

install
-------

with pip
~~~~~~~~~~~


::

	pip install playdeliver

from source
~~~~~~~~~~~

clone source:

::

    pip install -r requirements.txt
    python setup.py

licence
-------

MIT License
