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
        
        # Verify the dictionary contains all required keys
        required_keys = ['videoId', 'title', 'lengthSeconds', 'keywords', 'channelId', 
                        'shortDescription', 'thumbnail', 'viewCount', 'author']
        
        assert all(key in result for key in required_keys), "Result should contain all required keys"


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

    def test_get_video_transcript_no_captions(self, youtube_api):
        """Test that get_video_transcript raises an exception for videos without captions"""
        video_id = "v9ZApdKADxs"  # Video ID known to have no captions
        
        # Verify that an exception is raised when trying to get transcript for video without captions
        with pytest.raises(Exception):
            youtube_api.get_video_transcript(video_id)


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



    def test_get_trending_news_success(self, youtube_api):
        """Test that get_trending_news works and returns populated data"""
        
        # Call the function - this should not raise any exceptions
        result = youtube_api.get_trending_news()
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary contains the 'trending_news' key
        assert result.get('trending_news') is not None, "Result should contain 'trending_news' key"
        
        # Verify the trending_news value is a list
        assert isinstance(result.get('trending_news'), list), "Trending news should be a list"
        
        # Verify the trending_news list is not empty
        trending_news = result.get('trending_news')
        assert len(trending_news) > 0, "Trending news list should not be empty"
        assert trending_news, "Trending news list should be truthy (not empty)"