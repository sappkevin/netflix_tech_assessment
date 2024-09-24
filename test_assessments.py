import unittest
from unittest.mock import patch, MagicMock
from assessment1 import generate_root_report
from assessment2 import generate_folder_structure_report_csv
from assessment3 import copy_source_to_destination
from config import SOURCE_FOLDER_ID

class TestAssessments(unittest.TestCase):

    @patch('assessment1.get_drive_service')
    @patch('assessment1.list_files_and_folders')
    def test_generate_root_report(self, mock_list_files, mock_get_service):
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_list_files.return_value = [
            {'mimeType': 'application/vnd.google-apps.folder'},
            {'mimeType': 'application/vnd.google-apps.folder'},
            {'mimeType': 'application/vnd.google-apps.document'},
            {'mimeType': 'application/vnd.google-apps.spreadsheet'},
        ]

        result = generate_root_report()

        self.assertEqual(result['total_files'], 2)
        self.assertEqual(result['total_folders'], 2)
        self.assertEqual(result['total_items'], 4)

    @patch('assessment2.get_drive_service')
    @patch('assessment2.list_files_and_folders')
    @patch('assessment2.count_items_in_folder')
    def test_generate_folder_structure_report_csv(self, mock_count_items, mock_list_files, mock_get_service):
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_list_files.return_value = [
            {'name': 'Folder1', 'id': '1', 'mimeType': 'application/vnd.google-apps.folder'},
            {'name': 'Folder2', 'id': '2', 'mimeType': 'application/vnd.google-apps.folder'},
        ]
        mock_count_items.side_effect = [(10, 2), (5, 1), (15, 3)]  # Added one more tuple for the final count

        result = generate_folder_structure_report_csv()

        self.assertEqual(result['total_nested_folders'], 3)
        self.assertEqual(result['total_items'], 15)
        self.assertEqual(result['total_folders'], 3)
        mock_count_items.assert_called_with(mock_service, SOURCE_FOLDER_ID)

    @patch('assessment3.get_drive_service')
    @patch('assessment3.copy_folder_contents')
    def test_copy_source_to_destination(self, mock_copy_contents, mock_get_service):
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_copy_contents.return_value = None

        result = copy_source_to_destination()

        self.assertTrue(result)
        mock_copy_contents.assert_called_once()

if __name__ == '__main__':
    unittest.main()