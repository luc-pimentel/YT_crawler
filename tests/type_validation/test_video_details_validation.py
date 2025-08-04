import pytest
import json
import os
from pathlib import Path
from pydantic import ValidationError
import sys

# Add the yt_crawler package to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from yt_crawler.types.video_details import VideoDetailsResponse, VideoDetails, PlayerMicroformatRenderer
from yt_crawler import YoutubeAPI


class TestVideoDetailsValidation:
    """Comprehensive test suite for video details Pydantic model validation"""
    
    @pytest.fixture
    def sample_video_data(self):
        """Get real video details data from YouTube API for video ID 'gaH4g0l6f9w'"""
        video_id = "gaH4g0l6f9w"
        youtube_api = YoutubeAPI()
        
        try:
            # Make real API call to get video details
            video_data = youtube_api.get_video_details(video_id)
            return video_data
        except Exception as e:
            pytest.skip(f"Failed to fetch video details for {video_id}: {e}")
    
    def test_video_details_response_validation(self, sample_video_data):
        """Test that VideoDetailsResponse validates against real API data"""
        try:
            # Try Pydantic v2 first, fallback to v1
            try:
                validated_model = VideoDetailsResponse.model_validate(sample_video_data)
                print("Using Pydantic v2 for validation")
            except AttributeError:
                validated_model = VideoDetailsResponse.parse_obj(sample_video_data)
                print("Using Pydantic v1 for validation")
            
            # Basic structure validation
            assert isinstance(validated_model, VideoDetailsResponse)
            assert hasattr(validated_model, 'video_details')
            assert hasattr(validated_model, 'microformat')
            
            # Verify video_details structure
            assert isinstance(validated_model.video_details, VideoDetails)
            
        except ValidationError as e:
            pytest.fail(f"VideoDetailsResponse validation failed: {e}")
        except Exception as e:
            pytest.fail(f"Unexpected error during validation: {str(e)}")