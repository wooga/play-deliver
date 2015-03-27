play-deliver
============

Upload screenshots, metadata of your app to the Play Store using a
single command

deliver can upload app screenshots google play backend.

usage
-----

::
    Usage:

    playdeliver (--service-email=<e> --key=<k> | --credentials=<c>) upload <package> <output_dir>
    playdeliver (--service-email=<e> --key=<k> | --credentials=<c>) init <package> <output_dir>
    playdeliver (-h | --help)
    playdeliver --version

    Options:

      -h --help
        Show this screen.

      --version
        Show version.

      --service-email=<e>
        Account service email. Use this option together with `--key` to pass a 
        corresponding keyfile for user.

      --key=<k>
        Path to *.p12 keyfile for user specified with `service-email`

      --credentials=<c>
        Path to credentials json file. This file is a alternative solution to log
        into play. Download the file from play service administration page.

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
