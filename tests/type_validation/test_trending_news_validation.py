import pytest
import json
import os
from pathlib import Path
from pydantic import ValidationError
import sys

# Add the yt_crawler package to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from yt_crawler.types.trending_news import TrendingNewsResponse
from yt_crawler import YoutubeAPI


class TestTrendingNewsValidation:
    """Comprehensive test suite for trending news Pydantic model validation"""
    
    @pytest.fixture
    def sample_trending_news_data(self):
        """Get real trending news data from YouTube API"""
        youtube_api = YoutubeAPI()
        
        try:
            # Make real API call to get trending news
            trending_news_data = youtube_api.get_trending_news()
            return trending_news_data
        except Exception as e:
            pytest.skip(f"Failed to fetch trending news: {e}")
    
    def test_trending_news_response_validation(self, sample_trending_news_data):
        """Test that TrendingNewsResponse validates against real API data"""
        try:
            # Try Pydantic v2 first, fallback to v1
            try:
                validated_model = TrendingNewsResponse.model_validate(sample_trending_news_data)
                print("Using Pydantic v2 for validation")
            except AttributeError:
                validated_model = TrendingNewsResponse.parse_obj(sample_trending_news_data)
                print("Using Pydantic v1 for validation")
            
            # Basic structure validation
            assert isinstance(validated_model, TrendingNewsResponse)
            assert hasattr(validated_model, 'trending_news')
            assert isinstance(validated_model.trending_news, list)
            assert len(validated_model.trending_news) > 0
            
            print(f"Successfully validated {len(validated_model.trending_news)} trending news sections")
            
        except ValidationError as e:
            pytest.fail(f"TrendingNewsResponse validation failed: {e}")
        except Exception as e:
            pytest.fail(f"Unexpected error during validation: {str(e)}")