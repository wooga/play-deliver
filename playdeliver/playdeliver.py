#!/usr/bin/env python
"""starting point for the playdeliver tool."""

import os
import sys
from sync_command import SyncCommand
from oauth2client import client


def _load_key(location):
    if location is not None and os.path.isfile(location):
        f = open(location, 'rb')
        key = f.read()
        f.close()
        return key
    else:
        sys.exit("no key file found")


def execute(options):
    """execute the tool with given options."""
    # Load the key in PKCS 12 format that you downloaded from the Google APIs
    # Console when you created your Service account.
    package_name = options['<package>']
    source_directory = options['<output_dir>']

    if options['upload'] is True:
        upstream = True
    else:
        upstream = False

    if upstream is False:
        print(
            "Warning! Downloaded images are only previews!"
            "They may be to small for upload.")

    credentials = create_credentials(credentials_file=options['--credentials'],
                                     service_email=options['--service-email'],
                                     service_key=options['--key'])

    command = SyncCommand(
        package_name, source_directory, upstream, credentials)
    command.execute()


def create_credentials(credentials_file=None,
                       service_email=None,
                       service_key=None,
                       scope='https://www.googleapis.com/auth/androidpublisher'):
    """
    Create Google credentials object.

    If given credentials_file is None, try to retrieve file path from environment 
    or look up file in homefolder.
    """
    credentials = None
    if service_email is None and service_key is None:
        if credentials_file is None:
            # try load file from env
            key = 'PLAY_DELIVER_CREDENTIALS'
            if key in os.environ:
                credentials_file = os.environ[key]

        if credentials_file is None:
            # try to find the file in home
            path = os.path.expanduser('~/.playdeliver/credentials.json')
            if os.path.exists(path):
                credentials_file = path

        if credentials_file is not None:
            credentials = client.GoogleCredentials.from_stream(
                credentials_file)
            credentials = credentials.create_scoped(scope)
    else:
        credentials = client.SignedJwtAssertionCredentials(
            service_email, _load_key(service_key), scope=scope)
    return credentials
