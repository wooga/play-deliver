"""Module for SyncCommand class."""
from client import Client
from apiclient.discovery import build
import httplib2
import listing
import image


class SyncCommand(object):

    """The Sync command executes the up-/download of items from play."""

    def __init__(self, package_name, source_directory, upstream,
                 credentials, **options):
        """
        Create new SyncCommand with given params.

        package_name the app package to upload download items to
        credentials = a GoogleCredentials object
        source_directory = the directory to sync from/to
        upstream = uplaod or download items from/to play
        options = additional options
        """
        super(SyncCommand, self).__init__()
        self.package_name = package_name
        self.credentials = credentials
        self.source_directory = source_directory
        self.upstream = upstream
        self.options = options
        self._init_credentials()
        self._initialize_client()

    def _initialize_client(self):
        self.client = Client(self.package_name, self.service)

    def _init_credentials(self):
        http = httplib2.Http()
        http = self.credentials.authorize(http)

        self.service = build('androidpublisher', 'v2', http=http)

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
