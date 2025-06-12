import pytest
import sys
import os
import time
# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from yt_crawler import YoutubeAPI
from yt_crawler.youtube_news import categories_dict


class TestYoutubeNews:
    """Tests specifically for YouTube news functionality"""
    
    @pytest.fixture
    def youtube_api(self):
        """Create a YoutubeAPI instance for testing"""
        return YoutubeAPI()

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


    def test_get_trending_news_all_categories(self, youtube_api):
        """Test that get_trending_news works for all available categories"""
        
        for category in categories_dict.keys():
            # Call the function with each category
            result = youtube_api.get_trending_news(category=category)
            
            # Verify the result is a dictionary
            assert isinstance(result, dict), f"Result should be a dictionary for category '{category}'"
            
            # Verify the dictionary contains the 'trending_news' key
            assert result.get('trending_news') is not None, f"Result should contain 'trending_news' key for category '{category}'"
            
            # Verify the trending_news value is a list
            assert isinstance(result.get('trending_news'), list), f"Trending news should be a list for category '{category}'"
            
            # Verify the trending_news list is not empty
            trending_news = result.get('trending_news')
            assert len(trending_news) > 0, f"Trending news list should not be empty for category '{category}'"
            assert trending_news, f"Trending news list should be truthy (not empty) for category '{category}'"
            time.sleep(2)