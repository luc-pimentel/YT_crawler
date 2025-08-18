import pytest
import json
import os
from pathlib import Path
from pydantic import ValidationError
import sys

# Add the yt_crawler package to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from yt_crawler.types.playlist import PlaylistVideosResponse
from yt_crawler import YoutubeAPI


class TestPlaylistTypesValidation:
    """Comprehensive test suite for playlist Pydantic model validation"""
    
    @pytest.fixture
    def sample_playlist_data(self):
        """Get real playlist data from YouTube API"""
        youtube_api = YoutubeAPI()
        
        try:
            # Make real API call to get playlist videos using the same playlist ID from test_yt_playlist.py
            playlist_id = "PLZXffy-ZvjZlYVoiACyccatARtwXOyt48"
            playlist_data = youtube_api.get_playlist_videos(playlist_id)
            return playlist_data
        except Exception as e:
            pytest.skip(f"Failed to fetch playlist data: {e}")
    
    def test_playlist_videos_response_validation(self, sample_playlist_data):
        """Test that PlaylistVideosResponse validates against real API data"""
        try:
            # Try Pydantic v2 first, fallback to v1
            try:
                validated_model = PlaylistVideosResponse.model_validate(sample_playlist_data)
                print("Using Pydantic v2 for validation")
            except AttributeError:
                validated_model = PlaylistVideosResponse.parse_obj(sample_playlist_data)
                print("Using Pydantic v1 for validation")
            
            # Basic structure validation
            assert isinstance(validated_model, PlaylistVideosResponse)
            assert hasattr(validated_model, 'playlist_videos')
            assert isinstance(validated_model.playlist_videos, list)
            assert len(validated_model.playlist_videos) > 0
            
            print(f"Successfully validated {len(validated_model.playlist_videos)} playlist video items")
            
        except ValidationError as e:
            pytest.fail(f"PlaylistVideosResponse validation failed: {e}")
        except Exception as e:
            pytest.fail(f"Unexpected error during validation: {str(e)}")
