import pytest
import json
import os
from pathlib import Path
from pydantic import ValidationError
import sys

# Add the yt_crawler package to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from yt_crawler.types.comments import VideoCommentsResponse
from yt_crawler import YoutubeAPI


class TestVideoCommentsValidation:
    """Comprehensive test suite for video comments Pydantic model validation"""
    
    @pytest.fixture
    def sample_comments_data(self):
        """Get real video comments data from YouTube API for video ID 'gaH4g0l6f9w'"""
        video_id = "gaH4g0l6f9w"
        youtube_api = YoutubeAPI()
        
        try:
            # Make real API call to get video comments (limit to 50 for testing)
            comments_data = youtube_api.get_video_comments(video_id, n_comments=50)
            return comments_data
        except Exception as e:
            pytest.skip(f"Failed to fetch video comments for {video_id}: {e}")
    
    
    def test_video_comments_response_validation(self, sample_comments_data):
        """Test that VideoCommentsResponse validates against real data"""
        try:
            # Try Pydantic v2 first, fallback to v1
            try:
                validated_model = VideoCommentsResponse.model_validate(sample_comments_data)
                print("Using Pydantic v2 for validation")
            except AttributeError:
                validated_model = VideoCommentsResponse.parse_obj(sample_comments_data)
                print("Using Pydantic v1 for validation")
            
            # Basic structure validation
            assert isinstance(validated_model, VideoCommentsResponse)
            assert hasattr(validated_model, 'comments')
            assert isinstance(validated_model.comments, list)
            assert len(validated_model.comments) > 0
            
            print(f"Successfully validated {len(validated_model.comments)} comments")
            
        except ValidationError as e:
            pytest.fail(f"VideoCommentsResponse validation failed: {e}")
