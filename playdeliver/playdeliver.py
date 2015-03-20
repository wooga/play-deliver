#!/usr/bin/env python
"""starting point for the playdeliver tool."""

import os
import sys
from sync_command import SyncCommand


def _load_key(location):
    if location is not None and os.path.isfile(location):
        f = open(location, 'rb')
        key = f.read()
        f.close()
        return key
    else:
        sys.exit("no key file found")


def _fetch_service_mail(email=None):
    if email is not None:
        return email
    else:
        sys.exit("no service email provided")


def execute(options):
    """execute the tool with given options."""
    # Load the key in PKCS 12 format that you downloaded from the Google APIs
    # Console when you created your Service account.
    email = _fetch_service_mail(options['--service-email'])
    key = _load_key(options['--key'])
    package_name = options['<package-name>']
    source_directory = options['<output_dir>']

    if options['upload'] is True:
        upstream = True
    else:
        upstream = False

    if upstream is False:
        print(
            "Warning! Downloaded images are only previews!"
            "They may be to small for upload.")

    command = SyncCommand(package_name, email, key, source_directory, upstream)
    command.execute()
