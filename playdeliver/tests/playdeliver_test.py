"""Test for playdeliver module"""
import unittest
from oauth2client import client
from mock import Mock
from mock import patch

from playdeliver import playdeliver


class TestPlayDeliver(unittest.TestCase):

    """Test for playdeliver module"""

    def setUp(self):
        pass

    @patch('playdeliver.playdeliver.client')
    def test_create_credentials_with_service_email(self, client_mock):
        with patch('playdeliver.playdeliver._load_key', **{'method.return_value': 'a key'}):
            credentials = playdeliver.create_credentials(
                service_email='test@test.com', service_key='random_key')

        self.assertIsNotNone(credentials)
        assert client_mock.SignedJwtAssertionCredentials.called

    @patch('playdeliver.playdeliver.client')
    def test_create_credentials_with_service_email_file_in_env(self, client_mock):
        with patch.dict('os.environ', {'PLAY_DELIVER_CREDENTIALS': "some_file"}):
            with patch('playdeliver.playdeliver._load_key', **{'method.return_value': 'a key'}):
                credentials = playdeliver.create_credentials(
                    service_email='test@test.com', service_key='random_key')

        self.assertIsNotNone(credentials)
        assert client_mock.SignedJwtAssertionCredentials.called


    @patch('playdeliver.playdeliver.client')
    def test_create_credentials_with_credentials_file(self, client_mock):
        file_path = '/path/to/credentials.json'
        scope = 'https://www.googleapis.com/auth/androidpublisher'
        
        credentials_mock = Mock()
        client_mock.GoogleCredentials.from_stream.return_value = credentials_mock

        credentials = playdeliver.create_credentials(
            credentials_file=file_path, scope=scope)

        self.assertIsNotNone(credentials)
                
        client_mock.GoogleCredentials.from_stream.assert_called_with(file_path)
        credentials_mock.create_scoped.assert_called_with(scope)

    @patch('playdeliver.playdeliver.os')
    @patch('playdeliver.playdeliver.client')
    def test_create_credentials_with_credentials_from_home(self, client_mock, os_mock):
        file_path = '/home/some_user/.playdeliver/credentials.json'
        scope = 'https://www.googleapis.com/auth/androidpublisher'
        
        credentials_mock = Mock()
        client_mock.GoogleCredentials.from_stream.return_value = credentials_mock
        os_mock.path.expanduser.return_value = file_path
        os_mock.path.exists.return_value = True

        credentials = playdeliver.create_credentials(scope=scope)

        self.assertIsNotNone(credentials)
                
        client_mock.GoogleCredentials.from_stream.assert_called_with(file_path)
        credentials_mock.create_scoped.assert_called_with(scope)


    @patch('playdeliver.playdeliver.client')
    def test_create_credentials_with_credentials_from_env(self, client_mock):
        file_path = '/custom/location/credentials.json'
        scope = 'https://www.googleapis.com/auth/androidpublisher'
        
        credentials_mock = Mock()
        client_mock.GoogleCredentials.from_stream.return_value = credentials_mock
        
        with patch.dict('os.environ', {'PLAY_DELIVER_CREDENTIALS': file_path}):
            credentials = playdeliver.create_credentials(scope=scope)

        self.assertIsNotNone(credentials)
                
        client_mock.GoogleCredentials.from_stream.assert_called_with(file_path)
        credentials_mock.create_scoped.assert_called_with(scope)
