"""TestCase for Client class."""
import unittest
from mock import Mock

from playdeliver.client import Client


class TestClientMethods(unittest.TestCase):

    def setUp(self):
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


if __name__ == '__main__':
    unittest.main()
