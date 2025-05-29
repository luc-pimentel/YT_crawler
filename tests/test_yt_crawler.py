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


    def test_get_video_transcript_success(self, youtube_api):
        """Test that get_video_transcript works with a valid video ID and returns populated data"""
        video_id = "nUgGY18iTJw"
        
        # Call the function - this should not raise any exceptions
        result = youtube_api.get_video_transcript(video_id)
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary contains the 'transcript' key
        assert result.get('transcript') is not None, "Result should contain 'transcript' key"
        
        # Verify the transcript value is a list
        assert isinstance(result.get('transcript'), list), "Transcript should be a list"
        
        # Verify the transcript list is not empty
        transcript = result.get('transcript')
        assert len(transcript) > 0, "Transcript list should not be empty"
        assert transcript, "Transcript list should be truthy (not empty)"