play-deliver
============
.. image:: https://pypip.in/version/playdeliver/badge.svg?text=version
    :target: https://pypi.python.org/pypi/playdeliver/
    :alt: Latest Version

.. image:: https://pypip.in/license/playdeliver/badge.svg
    :target: https://pypi.python.org/pypi/playdeliver/
    :alt: License

.. image:: https://pypip.in/py_versions/playdeliver/badge.svg
    :target: https://pypi.python.org/pypi/playdeliver/
    :alt: Supported Python versions

.. image:: https://pypip.in/status/playdeliver/badge.svg
    :target: https://pypi.python.org/pypi/playdeliver/
    :alt: Development Status


Upload screenshots, metadata of your app to the Play Store using a
single command

deliver can upload app screenshots to google play backend.

usage
-----

.. code::
    Usage:

    playdeliver [options] upload <package> <output_dir>
    playdeliver [options] init <package> <output_dir>
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

google login
------------

Google login credentials can be passed in different ways. If the credentials
json file is not passed via `--credentials, --service-email and --service-key`, 
playdeliver will try to find the filepath either in a environment variable 
called `PLAY_DELIVER_CREDENTIALS` or in the user folder: 
`~/.playdeliver/credentials.json`.

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
