"""Module for SyncCommand class."""
from client import Client
from oauth2client import client
from apiclient.discovery import build
import httplib2
import listing
import image


class SyncCommand(object):

    """The Sync command executes the up-/download of items from play."""

    def __init__(self, package_name, source_directory, upstream,
                 service_mail=None, key=None,
                 credentials_file=None, **options):
        """
        Create new SyncCommand with given params.

        package_name the app package to upload download items to
        email = the service user email
        key = the service user key
        credentials_file = path to credentials json
        source_directory = the directory to sync from/to
        upstream = uplaod or download items from/to play
        options = additional options
        """
        super(SyncCommand, self).__init__()
        self.package_name = package_name
        self.service_mail = service_mail
        self.key = key
        self.credentials_file = credentials_file
        self.source_directory = source_directory
        self.upstream = upstream
        self.options = options
        self._init_credentials()
        self._initialize_client()

    def _initialize_client(self):
        self.client = Client(self.package_name, self.service)

    def _init_credentials(self):
        # Create an httplib2.Http object to handle our HTTP requests and
        # authorize it with the Credentials. Note that the first parameter,
        # service_account_name, is the Email address created for the Service
        # account. It must be the email address associated with
        # the key that was created.
        credentials = None
        scope = 'https://www.googleapis.com/auth/androidpublisher'
        if self.credentials_file is None:
            credentials = client.SignedJwtAssertionCredentials(
                self.service_mail,
                self.key,
                scope=scope)
        else:
            credentials = client.GoogleCredentials.from_stream(
                self.credentials_file)
            credentials = credentials.create_scoped(scope)

        http = httplib2.Http()
        http = credentials.authorize(http)

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
