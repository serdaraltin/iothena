import unittest
from unittest.mock import patch

import sys

from app.helpers.permission import PermissionService


class TestPermissionService(unittest.TestCase):
    def setUp(self):
        self.permission_service = PermissionService()

    @patch('os.geteuid')
    def test_check_if_root(self, mock_geteuid):
        mock_geteuid.return_value = 0
        self.assertTrue(self.permission_service.check_if_root())

        mock_geteuid.return_value = 1000
        self.assertFalse(self.permission_service.check_if_root())

    @patch('subprocess.run')
    @patch('os.geteuid')
    def test_run_as_root(self, mock_geteuid, mock_run):
        mock_geteuid.return_value = 1000

        with self.assertRaises(SystemExit):
            self.permission_service.run_as_root()

        mock_geteuid.return_value = 0
        self.assertTrue(self.permission_service.run_as_root())

    @patch('subprocess.run')
    @patch('os.geteuid')
    @patch('sys.exit')
    def test_elevate_to_root(self, mock_exit, mock_geteuid, mock_run):
        mock_geteuid.return_value = 1000
        sys.argv = ['test_permission.py', 'arg1', 'arg2']

        permission_service = PermissionService()
        permission_service.elevate_to_root()

        print(f"mock_run called: {mock_run.called}")
        if mock_run.called:
            print(f"mock_run call arguments: {mock_run.call_args}")

        expected_args = ['sudo', 'python3'] + sys.argv
        mock_run.assert_called_once_with(expected_args, check=True)

        mock_geteuid.return_value = 0
        permission_service.elevate_to_root()
        mock_run.assert_not_called()


    @patch('os.access')
    def test_check_permission_for_file(self, mock_access):
        mock_access.return_value = True
        self.assertTrue(self.permission_service.check_permission_for_file("/path/to/file"))

        mock_access.return_value = False
        self.assertFalse(self.permission_service.check_permission_for_file("/path/to/file"))


    @patch('os.chmod')
    @patch('os.access')
    @patch('os.geteuid')
    def test_ensure_permission_for_file(self, mock_geteuid, mock_access, mock_chmod):
        file_path = "/path/to/file"

        mock_access.return_value = True
        self.assertTrue(self.permission_service.ensure_permission_for_file(file_path))

        mock_access.return_value = False
        mock_geteuid.return_value = 0
        self.assertTrue(self.permission_service.ensure_permission_for_file(file_path))
        mock_chmod.assert_called_once_with(file_path, 0o600)

        mock_geteuid.return_value = 1000
        with self.assertRaises(SystemExit):
            self.permission_service.ensure_permission_for_file(file_path)

    @patch('subprocess.run')
    @patch('os.geteuid')
    def test_run_command_as_root(self, mock_geteuid, mock_run):
        """Test if commands are run with root privileges."""
        command = ['ls', '/root']

        # Simulate running as root
        mock_geteuid.return_value = 0  # UID 0 means root
        self.permission_service.run_command_as_root(command)
        mock_run.assert_called_once_with(command, check=True)  # Assert that the command was run

        # Simulate running as a normal user (not root)
        mock_geteuid.return_value = 1000  # Non-root user
        self.permission_service.run_command_as_root(command)
        mock_run.assert_called_once()  # Assert that no command should have been run


if __name__ == '__main__':
    unittest.main()
