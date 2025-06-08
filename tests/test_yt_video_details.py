import pytest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from yt_crawler import YoutubeAPI


class TestYoutubeVideoDetails:
    """Tests specifically for YouTube video details functionality"""
    
    @pytest.fixture
    def youtube_api(self):
        """Create a YoutubeAPI instance for testing"""
        return YoutubeAPI()
    
    def test_get_video_details_success(self, youtube_api):
        """Test that get_video_details works with a valid video ID and returns populated data"""
        video_id = "nUgGY18iTJw"
        
        # Call the function - this should not raise any exceptions
        result = youtube_api.get_video_details(video_id)
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary is not empty
        assert len(result) > 0, "Result should not be empty"
        assert result, "Result should be truthy (not empty)"
        
        # Verify the dictionary contains all required keys
        required_keys = ['videoId', 'title', 'lengthSeconds', 'keywords', 'channelId', 
                        'shortDescription', 'thumbnail', 'viewCount', 'author']
        
        assert all(key in result for key in required_keys), "Result should contain all required keys"