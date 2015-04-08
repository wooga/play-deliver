"""TestCase for Client class."""
import unittest
from mock import Mock

from playdeliver.client import Client


class TestClientMethods(unittest.TestCase):

    """Test Case Class for Client object."""

    def setUp(self):
        """Setup TestCase."""
        self.service_mock = Mock()
        self.edits_mock = Mock()

        self.service_mock.edits.return_value = self.edits_mock

        self.request_mock = Mock()
        self.edits_mock.insert.return_value = self.request_mock

        self.request_mock.execute.side_effect = [
            {'id': '1'}, {'id': '2'}]

        self.client = Client('com.test.app', self.service_mock)

    def test_build_params_without_editId(self):
        """Test of build params retrurns correct dict."""
        returned_params = self.client.build_params()
        self.assertEqual(
            returned_params, {'editId': None,
                              'packageName': 'com.test.app'})

    def test_build_params_with_editId(self):
        """Test of build params retrurns correct dict."""
        self.client.ensure_edit_id()

        returned_params = self.client.build_params()
        self.assertEqual(
            returned_params, {'editId': '1',
                              'packageName': 'com.test.app'})

    def test_build_params_with_custom_params(self):
        """Test of build params retrurns correct dict."""
        self.client.ensure_edit_id()

        returned_params = self.client.build_params({'foo': 'bar'})
        self.assertEqual(
            returned_params, {'editId': '1',
                              'packageName': 'com.test.app',
                              'foo': 'bar'})

    def test_ensure_edit_id(self):
        """Test if edit_id is created once when not set."""
        self.assertEqual(self.client.edit_id, None)

        self.client.ensure_edit_id()

        self.assertEqual(self.client.edit_id, '1')

        self.client.ensure_edit_id()

        self.assertEqual(self.client.edit_id, '1')

        self.client.edit_id = None
        self.client.ensure_edit_id()

        self.assertEqual(self.client.edit_id, '2')

    def test_commit(self):
        """Test if commit method executes commit."""
        self.client.ensure_edit_id()

        commit_mock = Mock()
        self.edits_mock.commit.return_value = commit_mock
        commit_mock.execute.return_value = {'id': '1'}

        self.client.commit()
        commit_mock.executes.assertCalled()
        self.assertEqual(self.client.edit_id, None)

    def test_list(self):
        """
        Test if list function of given service is executed.

        Should return unpacked list retrieved from service name.
        """
        service_method_impl = self._setup_service_request_mock(
            'apks', 'list', [{'apks': ['1', '2', '3']}])

        response = self.client.list('apks')
        self.assertEqual(response, ['1', '2', '3'])

        service_method_impl.assert_called_with(editId='1',
                                               packageName='com.test.app')

    def test_list_with_params(self):
        """
        Test if list function of given service is executed.

        Should return unpacked list retrieved from service name.
        """
        service_method_impl = self._setup_service_request_mock(
            'apks', 'list', [{'apks': ['1', '2', '3']}])

        response = self.client.list('apks', foo='bar')
        self.assertEqual(response, ['1', '2', '3'])

        service_method_impl.assert_called_with(editId='1',
                                               packageName='com.test.app',
                                               foo='bar')

    def test_list_with_params(self):
        """
        Test if list function of given service is executed.

        It should return empty list
        """
        service_method_impl = self._setup_service_request_mock(
            'apks', 'list', [{'foo': ['1', '2', '3']}])

        response = self.client.list('apks', foo='bar')
        self.assertEqual(response, [])

        service_method_impl.assert_called_with(editId='1',
                                               packageName='com.test.app',
                                               foo='bar')

    def test_upload(self):
        """Test if upload function of given service is executed."""
        service_method_impl = self._setup_service_request_mock(
            'apks', 'upload', [{'status': 'ok'}])

        response = self.client.upload('apks')
        self.assertEqual(response, {'status': 'ok'})

        service_method_impl.assert_called_with(editId='1',
                                               packageName='com.test.app')

    def test_upload_with_params(self):
        """Test if upload function of given service is executed."""
        service_method_impl = self._setup_service_request_mock(
            'apks', 'upload', [{'status': 'ok'}])

        response = self.client.upload('apks', foo='bar')
        self.assertEqual(response, {'status': 'ok'})

        service_method_impl.assert_called_with(editId='1',
                                               packageName='com.test.app',
                                               foo='bar')

    def test_update(self):
        """Test if update function of given service is executed."""
        service_method_impl = self._setup_service_request_mock(
            'apks', 'update', [{'status': 'ok'}])

        response = self.client.update('apks')
        self.assertEqual(response, {'status': 'ok'})

        service_method_impl.assert_called_with(editId='1',
                                               packageName='com.test.app')

    def test_update_with_params(self):
        """Test if update function of given service is executed."""
        service_method_impl = self._setup_service_request_mock(
            'apks', 'update', [{'status': 'ok'}])

        response = self.client.update('apks', foo='bar')
        self.assertEqual(response, {'status': 'ok'})

        service_method_impl.assert_called_with(editId='1',
                                               packageName='com.test.app',
                                               foo='bar')

    def test_deleteall(self):
        """Test if deleteall function of given service is executed."""
        service_method_impl = self._setup_service_request_mock(
            'apks', 'deleteall', [{'status': 'ok'}])

        response = self.client.deleteall('apks')
        self.assertEqual(response, {'status': 'ok'})

        service_method_impl.assert_called_with(editId='1',
                                               packageName='com.test.app')

    def test_deleteall_with_params(self):
        """Test if deleteall function of given service is executed."""
        service_method_impl = self._setup_service_request_mock(
            'apks', 'deleteall', [{'status': 'ok'}])

        response = self.client.deleteall('apks', foo='bar')
        self.assertEqual(response, {'status': 'ok'})

        service_method_impl.assert_called_with(editId='1',
                                               packageName='com.test.app',
                                               foo='bar')

    # Helper Methods
    def _setup_service_request_mock(
            self,  endpoint_name, method_name, side_effect):
        service_mock = Mock()
        request_mock = Mock()
        request_mock.execute.side_effect = side_effect

        endpoint = getattr(self.edits_mock, endpoint_name)
        endpoint.return_value = service_mock

        method = getattr(service_mock, method_name)
        method.return_value = request_mock

        return method


if __name__ == '__main__':
    unittest.main()
