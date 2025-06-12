import pytest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from yt_crawler import YoutubeAPI


class TestYoutubeAPI:
    """Simple tests to verify YoutubeAPI functions are working"""
    
    @pytest.fixture
    def youtube_api(self):
        """Create a YoutubeAPI instance for testing"""
        return YoutubeAPI()

    def test_get_trending_videos_success(self, youtube_api):
        """Test that get_trending_videos works and returns populated data"""
        
        # Call the function - this should not raise any exceptions
        result = youtube_api.get_trending_videos()
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary contains the 'trending' key
        assert result.get('trending') is not None, "Result should contain 'trending' key"
        
        # Verify the trending value is a list
        assert isinstance(result.get('trending'), list), "Trending should be a list"
        
        # Verify the trending list is not empty
        trending = result.get('trending')
        assert len(trending) > 0, "Trending list should not be empty"
        assert trending, "Trending list should be truthy (not empty)"