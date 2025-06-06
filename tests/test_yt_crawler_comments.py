import pytest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from yt_crawler import YoutubeAPI


class TestYoutubeAPIComments:
    """Tests for YouTube comments functionality"""
    
    @pytest.fixture
    def youtube_api(self):
        """Create a YoutubeAPI instance for testing"""
        return YoutubeAPI()

    def test_get_video_comments_success(self, youtube_api):
        """Test that get_video_comments works with a valid video ID and returns populated data"""
        video_id = "nUgGY18iTJw"
        
        # Call the function - this should not raise any exceptions
        result = youtube_api.get_video_comments(video_id)
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary contains the 'comments' key
        assert result.get('comments') is not None, "Result should contain 'comments' key"
        
        # Verify the comments value is a list
        assert isinstance(result.get('comments'), list), "Comments should be a list"
        
        # Verify the comments list is not empty
        comments = result.get('comments')
        assert len(comments) > 0, "Comments list should not be empty"
        assert comments, "Comments list should be truthy (not empty)"