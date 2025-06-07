import pytest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from yt_crawler import YoutubeAPI


class TestYoutubeSearch:
    """Tests for YouTube search functionality"""
    
    @pytest.fixture
    def youtube_api(self):
        """Create a YoutubeAPI instance for testing"""
        return YoutubeAPI()

    def test_search_success(self, youtube_api):
        """Test that search works with a valid search term and returns populated data"""
        search_term = "python is good"
        
        # Call the function - this should not raise any exceptions
        result = youtube_api.search(search_term)
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary contains the 'search_results' key
        assert result.get('search_results') is not None, "Result should contain 'search_results' key"
        
        # Verify the search_results value is a list
        assert isinstance(result.get('search_results'), list), "Search results should be a list"
        
        # Verify the search_results list is not empty
        search_results = result.get('search_results')
        assert len(search_results) > 0, "Search results list should not be empty"
        assert search_results, "Search results list should be truthy (not empty)"


    def test_search_result_item_structure(self, youtube_api):
        """Test that each search result item has the required keys"""
        search_term = "python is good"
        
        # Call the function - this should not raise any exceptions
        result = youtube_api.search(search_term)
        
        # Get the search results list
        search_results = result.get('search_results')
        
        # Ensure we have results to test
        assert search_results, "Search results should not be empty for structure testing"
        
        # Test that all items are dictionaries
        assert all(isinstance(item, dict) for item in search_results), "All search result items should be dictionaries"
        
        # Test that all items have the required keys
        assert all('videoId' in item for item in search_results), "All search result items should contain 'videoId' key"
        assert all('thumbnail' in item for item in search_results), "All search result items should contain 'thumbnail' key"
        assert all('title' in item for item in search_results), "All search result items should contain 'title' key"