import pytest
import json
import os
from pathlib import Path
from pydantic import ValidationError
import sys

# Add the yt_crawler package to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from yt_crawler.types.playlist_details import PlaylistDetailsResponse, PlaylistDetails
from yt_crawler import YoutubeAPI


class TestPlaylistDetailsValidation:
    """Comprehensive test suite for playlist details Pydantic model validation"""
    
    @pytest.fixture
    def sample_playlist_details_data(self):
        """Get real playlist details data from YouTube API"""
        youtube_api = YoutubeAPI()
        
        try:
            # Make real API call to get playlist details using the same playlist ID from other tests
            playlist_id = "PLZXffy-ZvjZlYVoiACyccatARtwXOyt48"
            playlist_details_data = youtube_api.get_playlist_details(playlist_id)
            return playlist_details_data
        except Exception as e:
            pytest.skip(f"Failed to fetch playlist details: {e}")
    
    def test_playlist_details_response_validation(self, sample_playlist_details_data):
        """Test that PlaylistDetailsResponse validates against real API data"""
        try:
            # Try Pydantic v2 first, fallback to v1
            try:
                validated_model = PlaylistDetailsResponse.model_validate(sample_playlist_details_data)
                print("Using Pydantic v2 for validation")
            except AttributeError:
                validated_model = PlaylistDetailsResponse.parse_obj(sample_playlist_details_data)
                print("Using Pydantic v1 for validation")
            
            # Basic structure validation
            assert isinstance(validated_model, PlaylistDetailsResponse)
            assert hasattr(validated_model, 'playlist_details')
            assert isinstance(validated_model.playlist_details, PlaylistDetails)
            
            # Verify nested structure
            playlist_details = validated_model.playlist_details
            assert hasattr(playlist_details, 'title')
            assert hasattr(playlist_details, 'metadata')
            
            # Verify title structure
            assert hasattr(playlist_details.title, 'dynamic_text_view_model')
            title_model = playlist_details.title.dynamic_text_view_model
            assert hasattr(title_model, 'text')
            assert hasattr(title_model.text, 'content')
            assert isinstance(title_model.text.content, str)
            assert len(title_model.text.content) > 0
            
            # Verify metadata structure
            assert hasattr(playlist_details.metadata, 'content_metadata_view_model')
            metadata_model = playlist_details.metadata.content_metadata_view_model
            assert hasattr(metadata_model, 'metadata_rows')
            assert isinstance(metadata_model.metadata_rows, list)
            assert len(metadata_model.metadata_rows) > 0
            
            print(f"Successfully validated playlist details with title: '{title_model.text.content}'")
            print(f"Metadata contains {len(metadata_model.metadata_rows)} metadata rows")
            
        except ValidationError as e:
            pytest.fail(f"PlaylistDetailsResponse validation failed: {e}")
        except Exception as e:
            pytest.fail(f"Unexpected error during validation: {str(e)}")
    
    def test_playlist_details_structure_completeness(self, sample_playlist_details_data):
        """Test that all expected nested structures are present and correctly typed"""
        try:
            # Try Pydantic v2 first, fallback to v1
            try:
                validated_model = PlaylistDetailsResponse.model_validate(sample_playlist_details_data)
            except AttributeError:
                validated_model = PlaylistDetailsResponse.parse_obj(sample_playlist_details_data)
            
            # Deep structure validation
            playlist_details = validated_model.playlist_details
            
            # Title structure validation
            title = playlist_details.title
            assert hasattr(title.dynamic_text_view_model, 'renderer_context')
            renderer_context = title.dynamic_text_view_model.renderer_context
            assert hasattr(renderer_context, 'logging_context')
            assert hasattr(renderer_context.logging_context, 'logging_directives')
            
            # Metadata structure validation
            metadata = playlist_details.metadata
            content_metadata = metadata.content_metadata_view_model
            assert hasattr(content_metadata, 'delimiter')
            assert hasattr(content_metadata, 'renderer_context')
            
            # Verify metadata parts structure
            for metadata_row in content_metadata.metadata_rows:
                assert hasattr(metadata_row, 'metadata_parts')
                assert isinstance(metadata_row.metadata_parts, list)
                
                for metadata_part in metadata_row.metadata_parts:
                    # Each metadata part should have either avatar_stack or text (or both)
                    has_avatar_stack = hasattr(metadata_part, 'avatar_stack') and metadata_part.avatar_stack is not None
                    has_text = hasattr(metadata_part, 'text') and metadata_part.text is not None
                    assert has_avatar_stack or has_text, "Metadata part should have either avatar_stack or text"
            
            print("All nested structures validated successfully")
            
        except ValidationError as e:
            pytest.fail(f"Playlist details structure validation failed: {e}")
        except Exception as e:
            pytest.fail(f"Unexpected error during structure validation: {str(e)}")
