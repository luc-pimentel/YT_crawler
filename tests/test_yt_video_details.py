import pytest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from yt_crawler import YoutubeAPI


class TestYoutubeVideoDetails:
    """Tests specifically for YouTube video details functionality"""
    
    @pytest.fixture
    def youtube_api(self) -> YoutubeAPI:
        """Create a YoutubeAPI instance for testing"""
        return YoutubeAPI()
    
    def test_get_video_details_success(self, youtube_api: YoutubeAPI):
        """Test that get_video_details works with a valid video ID and returns populated data"""
        video_id = "nUgGY18iTJw"
        
        # Call the function - this should not raise any exceptions
        result = youtube_api.get_video_details(video_id)
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary is not empty
        assert len(result) > 0, "Result should not be empty"
        assert result, "Result should be truthy (not empty)"
        
        # Verify the top-level structure contains both required sections
        assert 'videoDetails' in result, "Result should contain 'videoDetails' key"
        assert 'microformat' in result, "Result should contain 'microformat' key"
        
        # Verify videoDetails section contains all required keys
        video_details = result['videoDetails']
        required_video_keys = ['videoId', 'title', 'lengthSeconds', 'keywords', 'channelId', 
                              'shortDescription', 'thumbnail', 'viewCount', 'author']
        
        assert all(key in video_details for key in required_video_keys), \
            "videoDetails should contain all required keys"
    
    def test_get_video_details_microformat(self, youtube_api: YoutubeAPI):
        """Test that microformat section contains all required playerMicroformatRenderer keys"""
        video_id = "nUgGY18iTJw"
        
        # Call the function
        result = youtube_api.get_video_details(video_id)
        
        # Verify microformat structure
        assert 'microformat' in result, "Result should contain 'microformat' key"
        microformat = result['microformat']
        
        assert 'playerMicroformatRenderer' in microformat, \
            "microformat should contain 'playerMicroformatRenderer' key"
        
        # Verify playerMicroformatRenderer contains all required keys
        player_microformat = microformat['playerMicroformatRenderer']
        required_microformat_keys = [
            'thumbnail', 'embed', 'title', 'lengthSeconds', 'ownerProfileUrl', 
            'externalChannelId', 'isFamilySafe', 'availableCountries', 'isUnlisted', 
            'hasYpcMetadata', 'viewCount', 'category', 'publishDate', 'ownerChannelName', 
            'uploadDate', 'isShortsEligible', 'externalVideoId', 'likeCount', 'canonicalUrl'
        ]
        
        assert all(key in player_microformat for key in required_microformat_keys), \
            "playerMicroformatRenderer should contain all required keys"