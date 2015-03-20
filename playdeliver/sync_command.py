"""Module for SyncCommand class."""
from client import Client
from oauth2client import client
import listing
import image


class SyncCommand(object):

    """The Sync command executes the up-/download of items from play."""

    def __init__(self, package_name, service_mail, key,
                 source_directory, upstream=False, **options):
        """
        Create new SyncCommand with given params.

        package_name the app package to upload download items to
        email = the service user email
        key = the service user key
        source_directory = the directory to sync from/to
        upstream = uplaod or download items from/to play
        options = additional options
        """
        super(SyncCommand, self).__init__()
        self.package_name = package_name
        self.service_mail = service_mail
        self.key = key
        self.source_directory = source_directory
        self.upstream = upstream
        self.options = options
        self._initialize_client()

    def _initialize_client(self):
        self.client = Client(self.package_name, self.service_mail, self.key)

    def execute(self):
        """Execute the command."""
        try:
            if self.upstream:
                listing.upload(self.client, self.source_directory)
                image.upload(self.client, self.source_directory)
                self.client.commit()
            else:
                listing.download(self.client, self.source_directory)
                image.download(self.client, self.source_directory)

        except client.AccessTokenRefreshError:
            print(
                'The credentials have been revoked or expired, please re-run'
                'the application to re-authorize')
