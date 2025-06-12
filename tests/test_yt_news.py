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

    def _validate_trending_news_item_structure(self, item, context=""):
        """Helper method to validate the structure of a single trending news item"""
        # Verify each item is a dictionary
        assert isinstance(item, dict), f"Each trending news item should be a dictionary{context}"
        
        # Verify required keys exist
        assert 'title' in item, f"Each trending news item should have a 'title' key{context}"
        assert 'contents' in item, f"Each trending news item should have a 'contents' key{context}"
        

    def test_get_trending_news_success(self, youtube_api):
        """Test that get_trending_news works and returns populated data with correct structure"""
        
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
        
        # Validate structure of each item in the trending news list
        for i, item in enumerate(trending_news):
            self._validate_trending_news_item_structure(item, f" (item {i})")

    def test_get_trending_news_all_categories(self, youtube_api):
        """Test that get_trending_news works for all available categories with correct item structure"""
        
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
            
            # Validate structure of each item in the trending news list
            for i, item in enumerate(trending_news):
                self._validate_trending_news_item_structure(item, f" (category '{category}', item {i})")
            
            time.sleep(2)

    def test_trending_news_item_structure_detailed(self, youtube_api):
        """Dedicated test for validating the detailed structure of trending news items"""
        
        # Get trending news for default category
        result = youtube_api.get_trending_news()
        trending_news = result.get('trending_news', [])
        
        # Ensure we have at least one item to test
        assert len(trending_news) > 0, "Need at least one trending news item for structure testing"
        
        # Test the first item in detail
        first_item = trending_news[0]
        
        # Basic structure validation
        self._validate_trending_news_item_structure(first_item)
        
        # Additional detailed checks
        assert len(first_item['title']) > 0, "Title should have content"
        assert len(first_item['contents']) > 0, "Contents should have content"
        
        # Verify no unexpected None values
        assert first_item['title'] is not None, "Title should not be None"
        assert first_item['contents'] is not None, "Contents should not be None"
        
        # Test that all items have consistent structure
        for i, item in enumerate(trending_news):
            assert set(item.keys()) >= {'title', 'contents'}, f"Item {i} missing required keys"