import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load_data.load_sheet import load_to_sheets, authenticate_google_sheets, prepare_data_for_upload

class TestLoadSheet(unittest.TestCase):

    @patch('utils.load_data.load_sheet.build')
    @patch('utils.load_data.load_sheet.service_account.Credentials.from_service_account_file')
    def test_authenticate_google_sheets(self, mock_creds, mock_build):
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_creds.return_value = MagicMock()

        service = authenticate_google_sheets()

        mock_build.assert_called_with('sheets', 'v4', credentials=mock_creds.return_value)
        self.assertEqual(service, mock_service)

    def test_prepare_data_for_upload(self):
        data = {'col1': [1, 2], 'col2': [3, 4]}
        df = pd.DataFrame(data)

        result = prepare_data_for_upload(df)

        expected_result = [['col1', 'col2'], [1, 3], [2, 4]]
        self.assertEqual(result, expected_result)

    @patch('utils.load_data.load_sheet.authenticate_google_sheets')
    def test_load_to_sheets(self, mock_authenticate_google_sheets):
        data = {'col1': [1, 2], 'col2': [3, 4]}
        df = pd.DataFrame(data)

        mock_service = MagicMock()
        mock_authenticate_google_sheets.return_value = mock_service
        mock_service.spreadsheets().values().update.return_value.execute.return_value = {'updatedRows': 2}

        result = load_to_sheets(df)

        self.assertIsNotNone(result)
        mock_service.spreadsheets().values().update.assert_called_once()

if __name__ == '__main__':
    unittest.main()