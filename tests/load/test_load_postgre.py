import unittest
import re
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load_data.load_postgre import load_to_postgres, create_table_if_not_exists, insert_or_update_data, establish_connection

DB_CONFIG = {
    "dbname": "fashionstudiodb",
    "user": "nurrizkyaj",
    "password": "fsdb",
    "host": "localhost",
    "port": "5432"
}

class TestLoadPostgre(unittest.TestCase):
    @patch('utils.load_data.load_postgre.psycopg2.connect')
    def test_establish_connection(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        connection, cursor = establish_connection()

        self.assertEqual(connection, mock_connection)
        self.assertEqual(cursor, mock_cursor)
        mock_connect.assert_called_once_with(**DB_CONFIG)
        mock_connection.cursor.assert_called_once()

    @patch('utils.load_data.load_postgre.establish_connection')
    def test_create_table_if_not_exists(self, mock_establish_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_establish_connection.return_value = (mock_connection, mock_cursor)

        create_table_if_not_exists(mock_cursor, 'test_table')

        expected_query = """
        CREATE TABLE IF NOT EXISTS test_table (
            id SERIAL PRIMARY KEY,
            title TEXT UNIQUE,
            price FLOAT,
            rating FLOAT,
            colors INT,
            size TEXT,
            gender TEXT,
            timestamp TIMESTAMP
        );
        """

        expected_query = re.sub(r'\s+', ' ', expected_query.strip())
        actual_query = re.sub(r'\s+', ' ', mock_cursor.execute.call_args[0][0].strip())

        self.assertEqual(expected_query, actual_query)

    @patch('utils.load_data.load_postgre.establish_connection')
    def test_insert_or_update_data(self, mock_establish_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_establish_connection.return_value = (mock_connection, mock_cursor)

        data = {'title': ['Item1', 'Item2'], 'price': [100.0, 200.0], 'rating': [4.5, 3.5], 
                'colors': [2, 3], 'size': ['L', 'M'], 'gender': ['M', 'F'], 'timestamp': ['2025-05-21', '2025-05-22']}
        df = pd.DataFrame(data)

        insert_or_update_data(mock_cursor, 'test_table', df)

        mock_cursor.execute.assert_called()

    @patch('utils.load_data.load_postgre.establish_connection')
    def test_load_to_postgres(self, mock_establish_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_establish_connection.return_value = (mock_connection, mock_cursor)

        data = {'title': ['Item1', 'Item2'], 'price': [100.0, 200.0], 'rating': [4.5, 3.5], 
                'colors': [2, 3], 'size': ['L', 'M'], 'gender': ['M', 'F'], 'timestamp': ['2025-05-21', '2025-05-22']}
        df = pd.DataFrame(data)

        load_to_postgres(df, 'test_table')

        mock_establish_connection.assert_called_once()
        mock_cursor.execute.assert_called()

if __name__ == '__main__':
    unittest.main()