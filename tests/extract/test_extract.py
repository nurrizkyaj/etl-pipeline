import unittest
from unittest.mock import patch, Mock
from utils.extract_data.extract import scrape_page, generate_urls, scrape_main
import requests

class TestExtractFunctions(unittest.TestCase):

    @patch('utils.extract_data.extract.requests.get')
    def test_scrape_page(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<html><body><div class="collection-card"><h3 class="product-title">Test Product</h3><span class="price">$100</span></div></body></html>'
        mock_get.return_value = mock_response

        url = 'https://fashion-studio.dicoding.dev/'
        
        result = scrape_page(url)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Title"], "Test Product")
        self.assertEqual(result[0]["Price"], "100")
        self.assertEqual(result[0]["Rating"], "Invalid")
        self.assertEqual(result[0]["Colors"], "N/A")
        self.assertEqual(result[0]["Size"], "N/A")
        self.assertEqual(result[0]["Gender"], "N/A")

    def test_generate_urls(self):
        result = generate_urls(3)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "https://fashion-studio.dicoding.dev/")
        self.assertEqual(result[1], "https://fashion-studio.dicoding.dev/page2")
        self.assertEqual(result[2], "https://fashion-studio.dicoding.dev/page3")

    @patch('utils.extract_data.extract.scrape_page')
    def test_scrape_main(self, mock_scrape_page):
        mock_scrape_page.return_value = [{"Title": "Product 1", "Price": "100", "Rating": "5", "Colors": "Red", "Size": "M", "Gender": "Unisex", "Timestamp": "2025-05-22"}]
        
        result = scrape_main(2)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["Title"], "Product 1")
        self.assertEqual(result[0]["Price"], "100")

if __name__ == '__main__':
    unittest.main()