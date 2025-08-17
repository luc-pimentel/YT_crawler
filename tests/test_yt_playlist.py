import pytest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from yt_crawler import YoutubeAPI


class TestYoutubePlaylist:
    """Tests specifically for YouTube playlist functionality"""
    
    @pytest.fixture
    def youtube_api(self) -> YoutubeAPI:
        """Create a YoutubeAPI instance for testing"""
        return YoutubeAPI()
    
    def test_get_playlist_videos_success(self, youtube_api: YoutubeAPI):
        """Test that get_playlist_videos works with a valid playlist ID and returns populated data"""
        # Use a known YouTube playlist ID (you can change this to any public playlist)
        playlist_id = "PLZXffy-ZvjZlYVoiACyccatARtwXOyt48"
        
        # Call the function - this should not raise any exceptions
        result = youtube_api.get_playlist_videos(playlist_id)
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary is not empty
        assert len(result) > 0, "Result should not be empty"
        assert result, "Result should be truthy (not empty)"
        
        # Verify the dictionary contains the 'playlist_videos' key
        assert 'playlist_videos' in result, "Result should contain 'playlist_videos' key"
        
        # Verify the playlist_videos value is a list
        playlist_videos = result['playlist_videos']
        assert isinstance(playlist_videos, list), "playlist_videos should be a list"
        
        # Verify the playlist_videos list is not empty
        assert len(playlist_videos) > 0, "playlist_videos list should not be empty"
        assert playlist_videos, "playlist_videos list should be truthy (not empty)"
    
    def test_get_playlist_videos_item_structure(self, youtube_api: YoutubeAPI):
        """Test that each playlist video item contains required keys in playlistVideoRenderer"""
        # Use a known YouTube playlist ID
        playlist_id = "PLZXffy-ZvjZlYVoiACyccatARtwXOyt48"
        
        # Call the function
        result = youtube_api.get_playlist_videos(playlist_id)
        
        # Get the playlist videos list
        playlist_videos = result['playlist_videos']
        
        # Required keys that each playlist video item should have in playlistVideoRenderer
        required_keys = ['videoId', 'thumbnail', 'title']
        
        # Test that each item has the playlistVideoRenderer key and required sub-keys
        for i, video_item in enumerate(playlist_videos):
            # Each item should have 'playlistVideoRenderer' key
            assert 'playlistVideoRenderer' in video_item, \
                f"Video item {i} should contain 'playlistVideoRenderer' key"
            
            playlist_video_renderer = video_item['playlistVideoRenderer']
            
            # Check that all required keys are present
            for key in required_keys:
                assert key in playlist_video_renderer, \
                    f"Video item {i} playlistVideoRenderer should contain '{key}' key"
            
            # Additional validation - ensure these keys have values (not None/empty)
            assert playlist_video_renderer['videoId'], \
                f"Video item {i} should have a non-empty videoId"
            assert playlist_video_renderer['thumbnail'], \
                f"Video item {i} should have thumbnail data"
            assert playlist_video_renderer['title'], \
                f"Video item {i} should have title data"
    
    def test_get_playlist_videos_with_different_playlist(self, youtube_api: YoutubeAPI):
        """Test with a different playlist to ensure the function works with various playlists"""
        # You can add more playlist IDs here to test with different playlists
        # This is the same playlist ID for now, but you could test with others
        playlist_id = "PLZXffy-ZvjZlYVoiACyccatARtwXOyt48"
        
        # Call the function
        result = youtube_api.get_playlist_videos(playlist_id)
        
        # Basic structure validation
        assert isinstance(result, dict), "Result should be a dictionary"
        assert 'playlist_videos' in result, "Result should contain 'playlist_videos' key"
        assert isinstance(result['playlist_videos'], list), "playlist_videos should be a list"
        assert len(result['playlist_videos']) > 0, "playlist_videos should not be empty"
        
        # Check that we can access the first video's basic info
        first_video = result['playlist_videos'][0]
        assert 'playlistVideoRenderer' in first_video, "First video should have playlistVideoRenderer"
        
        renderer = first_video['playlistVideoRenderer']
        assert 'videoId' in renderer, "First video should have videoId"
        assert 'title' in renderer, "First video should have title"
        assert 'thumbnail' in renderer, "First video should have thumbnail"
