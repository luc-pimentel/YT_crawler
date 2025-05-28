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
    
    def test_search_works(self, youtube_api):
        """Test that search function works without errors"""
        result = youtube_api.search("python")
        assert result is not None
        assert len(result) > 0
    
    def test_get_full_video_info_works(self, youtube_api):
        """Test that get_full_video_info function works without errors"""
        # Using the video ID from your notebook example
        video_id = "_uQrJ0TkZlc"
        result = youtube_api.get_full_video_info(video_id)
        assert result is not None
        assert len(result) > 0
    
    def test_search_channel_works(self, youtube_api):
        """Test that search_channel function works without errors"""
        result = youtube_api.search_channel("Mr beast")
        assert result is not None
        assert len(result) > 0