import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load_data.load_csv import load_csv

class TestLoadCSV(unittest.TestCase):

    @patch('utils.load_data.load_csv.pd.DataFrame.to_csv', side_effect=Exception("Test error"))
    @patch('utils.load_data.load_csv.logging')
    def test_load_csv_error(self, mock_logging, mock_to_csv):
        df = pd.DataFrame({
            'Title': ['Product 1'],
            'Price': [100],
            'Rating': [4.5],
            'Colors': ['Red'],
            'Size': ['M'],
            'Gender': ['Unisex'],
            'Timestamp': ['2025-05-22']
        })

        with self.assertRaises(Exception):
            load_csv(df, "test_products.csv")

        mock_logging.error.assert_called_with("An error occurred while saving the data: Test error")

    @patch('utils.load_data.load_csv.pd.DataFrame.to_csv')
    @patch('utils.load_data.load_csv.logging')
    def test_load_csv_success(self, mock_logging, mock_to_csv):
        df = pd.DataFrame({
            'Title': ['Product 1'],
            'Price': [100],
            'Rating': [4.5],
            'Colors': ['Red'],
            'Size': ['M'],
            'Gender': ['Unisex'],
            'Timestamp': ['2025-05-22']
        })
        
        load_csv(df, "test_products.csv")
        
        mock_to_csv.assert_called_once_with("test_products.csv", index=False, encoding='utf-8')
        
        mock_logging.info.assert_called_with("Data successfully saved in test_products.csv")

if __name__ == '__main__':
    unittest.main()