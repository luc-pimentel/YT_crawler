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
        trending = result.get('trending', [])
        assert len(trending) > 0, "Trending list should not be empty"
        assert trending, "Trending list should be truthy (not empty)"


    @pytest.mark.parametrize("category", ['now', 'music', 'gaming', 'movies'])
    def test_get_trending_videos_all_categories(self, youtube_api, category):
        """Test that get_trending_videos works for all categories and returns properly structured data"""
        
        # Define required keys that each video item should contain
        required_keys = ['videoId', 'title', 'viewCountText', 
                        'publishedTimeText', 'thumbnail', 'avatar']
        
        # Call the function - this should not raise any exceptions
        result = youtube_api.get_trending_videos(category=category)
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), f"Result should be a dictionary for category '{category}'"
        
        # Verify the dictionary contains the 'trending' key
        assert result.get('trending') is not None, f"Result should contain 'trending' key for category '{category}'"
        
        # Verify the trending value is a list
        assert isinstance(result.get('trending'), list), f"Trending should be a list for category '{category}'"
        
        # Verify the trending list is not empty
        trending = result.get('trending', [])
        assert len(trending) > 0, f"Trending list should not be empty for category '{category}'"
        assert trending, f"Trending list should be truthy (not empty) for category '{category}'"
        
        # Validate each video item in the trending list
        for i, video in enumerate(trending):
            assert isinstance(video, dict), f"Video item {i} should be a dictionary for category '{category}'"
            
            # Check that each video contains all required keys
            for key in required_keys:
                assert key in video, f"Video item {i} missing required key '{key}' for category '{category}'"
                # Ensure the key has a value (not None or empty string for critical fields)
                if key in ['videoId', 'title', 'channelId', 'author']:
                    assert video[key], f"Video item {i} has empty/None value for critical key '{key}' for category '{category}'"
