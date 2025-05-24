import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.transform_data.transform import check_data_validity, transform_data

class TestTransformFunctions(unittest.TestCase):

    def test_check_data_validity_valid_data(self):
        data = [{
            'Title': 'Product 1',
            'Price': '100',
            'Rating': '5.0',
            'Colors': 'Red'
        }]
        
        result = check_data_validity(data)
        
        self.assertTrue(result)

    def test_check_data_validity_missing_column(self):
        data = [{
            'Title': 'Product 1',
            'Price': '100',
            'Rating': '5.0'
        }]
        
        result = check_data_validity(data)
        
        self.assertFalse(result)

    @patch('utils.transform_data.transform.check_data_validity')
    def test_transform_data_success(self, mock_check_validity):
        mock_check_validity.return_value = True
        
        data = [{
            'Title': 'Product 1',
            'Price': '100',
            'Rating': '5.0',
            'Colors': 'Red',
            'Size': 'M',
            'Gender': 'Unisex',
            'Timestamp': '2025-05-22'
        }]
        
        transformed_df = transform_data(data)
        
        self.assertEqual(transformed_df["Price"].iloc[0], 1600000)
        self.assertEqual(transformed_df["Rating"].iloc[0], 5.0)
        self.assertEqual(transformed_df["Colors"].iloc[0], 0)
        self.assertEqual(len(transformed_df), 1)

    @patch('utils.transform_data.transform.check_data_validity')
    def test_transform_data_empty_data(self, mock_check_validity):
        mock_check_validity.return_value = False
        
        transformed_df = transform_data([])
        
        self.assertTrue(transformed_df.empty)

    def test_transform_data_invalid_rating(self):
        data = [{
            'Title': 'Product 1',
            'Price': '100',
            'Rating': 'Invalid Rating',
            'Colors': 'Red',
            'Size': 'M',
            'Gender': 'Unisex',
            'Timestamp': '2025-05-22'
        }]
        
        transformed_df = transform_data(data)
        
        self.assertTrue(transformed_df.empty)

    def test_transform_data_drop_duplicates(self):
        data = [{
            'Title': 'Product 1',
            'Price': '100',
            'Rating': '5.0',
            'Colors': 'Red',
            'Size': 'M',
            'Gender': 'Unisex',
            'Timestamp': '2025-05-22'
        }, {
            'Title': 'Product 1',
            'Price': '100',
            'Rating': '5.0',
            'Colors': 'Red',
            'Size': 'M',
            'Gender': 'Unisex',
            'Timestamp': '2025-05-22'
        }]
        
        transformed_df = transform_data(data)
        
        self.assertEqual(len(transformed_df), 1)

if __name__ == '__main__':
    unittest.main()