import pytest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from yt_crawler.utils import extract_youtube_initial_data
from yt_crawler.config import HEADERS


class TestExtractYoutubeInitialData:
    """Test suite for extract_youtube_initial_data function"""
    
    def test_extract_youtube_initial_data_ytInitialPlayerResponse_with_headers(self):
        """Test extracting ytInitialPlayerResponse with headers"""
        video_id = "nUgGY18iTJw"
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Call the function with headers
        result = extract_youtube_initial_data(url, 'ytInitialPlayerResponse', HEADERS)
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary is not empty
        assert len(result) > 0, "Result should not be empty"
        assert result, "Result should be truthy (not empty)"
    
    def test_extract_youtube_initial_data_ytInitialPlayerResponse_without_headers(self):
        """Test extracting ytInitialPlayerResponse without headers"""
        video_id = "nUgGY18iTJw"
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Call the function without headers (default None)
        result = extract_youtube_initial_data(url, 'ytInitialPlayerResponse')
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary is not empty
        assert len(result) > 0, "Result should not be empty"
        assert result, "Result should be truthy (not empty)"
    
    def test_extract_youtube_initial_data_ytInitialData_with_headers(self):
        """Test extracting ytInitialData with headers"""
        url = "https://www.youtube.com/results?search_query=python"
        
        # Call the function with headers
        result = extract_youtube_initial_data(url, 'ytInitialData', HEADERS)
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary is not empty
        assert len(result) > 0, "Result should not be empty"
        assert result, "Result should be truthy (not empty)"
    
    def test_extract_youtube_initial_data_ytInitialData_without_headers(self):
        """Test extracting ytInitialData without headers"""
        url = "https://www.youtube.com/results?search_query=python"
        
        # Call the function without headers (default None)
        result = extract_youtube_initial_data(url, 'ytInitialData')
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary is not empty
        assert len(result) > 0, "Result should not be empty"
        assert result, "Result should be truthy (not empty)"