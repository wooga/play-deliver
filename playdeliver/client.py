"""Module with Client class to access google api."""

from apiclient.discovery import build
import httplib2
from oauth2client import client


class Client(object):

    """
    Client object which handles google api edits.

    It hold the service user credentials and app package name.
    """

    def __init__(self, package_name, email, key):
        """
        create new client object.

        package_name = the app package you want to access
        email = the service user email
        key = the service user key
        """
        super(Client, self).__init__()
        self.package_name = package_name
        self.email = email
        self.key = key
        self.edit_id = None
        self._init_credentials()

    def list(self, service_name, **params):
        """
        convinent access method for list.

        service_name describes the endpoint to call
        the `list` function on.

        images.list or apks.list.
        """
        result = self._invoke_call(service_name, 'list', **params)
        if result is not None:
            return result.get(service_name, list())
        return list()

    def update(self, service_name, **params):
        """
        convinent access method for update.

        service_name describes the endpoint to call
        the `update` function on.

        images.update or apks.update.
        """
        return self._invoke_call(service_name, 'update', **params)

    def deleteall(self, service_name, **params):
        """
        convinent access method for deleteall.

        service_name describes the endpoint to call
        the `deleteall` function on.

        images.deleteall or apks.deleteall.
        """
        return self._invoke_call(service_name, 'deleteall', **params)

    def upload(self, service_name, **params):
        """
        convinent access method for upload.

        service_name describes the endpoint to call
        the `upload` function on.

        images.upload or apks.upload.
        """
        return self._invoke_call(service_name, 'upload', **params)

    def commit(self):
        """commit current edits."""
        request = self.edits().commit(**self.build_params()).execute()

        print 'Edit "%s" has been committed' % (request['id'])
        self.edit_id = None

    def _invoke_call(self, service_name, function_name, **params):
        self.ensure_edit_id()
        params = self.build_params(params)
        service_impl = getattr(self.edits(), service_name)
        method = getattr(service_impl(), function_name)

        if method and callable(method):
            return method(**params).execute()
        pass
        return None

    def build_params(self, params={}):
        """
        build a params dictionary with current.

        editId and packageName. use optional params parameter
        to merge additional params into resulting dictionary.
        """
        z = params.copy()
        z.update({'editId': self.edit_id, 'packageName': self.package_name})
        return z

    def edits(self):
        """Return current edits object."""
        return self.service.edits()

    def ensure_edit_id(self):
        """create edit id if edit id is None."""
        if self.edit_id is None:
            edit_request = self.edits().insert(
                body={}, packageName=self.package_name)
            result = edit_request.execute()
            self.edit_id = result['id']

    def _init_credentials(self):
        # Create an httplib2.Http object to handle our HTTP requests and
        # authorize it with the Credentials. Note that the first parameter,
        # service_account_name, is the Email address created for the Service
        # account. It must be the email address associated with
        # the key that was created.
        credentials = client.SignedJwtAssertionCredentials(
            self.email,
            self.key,
            scope='https://www.googleapis.com/auth/androidpublisher')

        http = httplib2.Http()
        http = credentials.authorize(http)

        self.service = build('androidpublisher', 'v2', http=http)
