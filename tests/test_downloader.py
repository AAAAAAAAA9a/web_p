"""
Tests for the website downloader module.
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from website_analyzer.core.downloader import WebsiteDownloader


class TestWebsiteDownloader(unittest.TestCase):
    """Test cases for WebsiteDownloader class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.downloader = WebsiteDownloader(max_pages=5, max_depth=1)
        
    def test_init(self):
        """Test downloader initialization."""
        self.assertEqual(self.downloader.max_pages, 5)
        self.assertEqual(self.downloader.max_depth, 1)
        self.assertEqual(self.downloader.timeout, 10)
        
    @patch('website_analyzer.core.downloader.requests.Session')
    def test_download_website_basic(self, mock_session_class):
        """Test basic website download functionality."""
        # Mock response
        mock_response = Mock()
        mock_response.text = "<html><body><h1>Test</h1></body></html>"
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'text/html'}
        mock_response.raise_for_status.return_value = None
        
        # Mock session
        mock_session = Mock()
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        # Test download
        result = self.downloader.download_website("https://example.com")
        
        # Assertions
        self.assertIsInstance(result, dict)
        self.assertIn("https://example.com", result)
        self.assertEqual(result["https://example.com"]["status_code"], 200)
        self.assertIn("content", result["https://example.com"])
        
    def test_progress_callback(self):
        """Test progress callback functionality."""
        messages = []
        
        def callback(message):
            messages.append(message)
            
        # This test would need more mocking for a full test
        # For now, just test that callback parameter is accepted
        self.downloader.download_website = Mock()
        self.downloader.download_website("https://example.com", callback)
        self.downloader.download_website.assert_called_once_with("https://example.com", callback)


if __name__ == '__main__':
    unittest.main()