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
    
    def test_get_video_details_success(self, youtube_api):
        """Test that get_video_details works with a valid video ID and returns populated data"""
        video_id = "nUgGY18iTJw"
        
        # Call the function - this should not raise any exceptions
        result = youtube_api.get_video_details(video_id)
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary is not empty
        assert len(result) > 0, "Result should not be empty"
        assert result, "Result should be truthy (not empty)"


    def test_get_video_transcript_success(self, youtube_api):
        """Test that get_video_transcript works with a valid video ID and returns populated data"""
        video_id = "nUgGY18iTJw"
        
        # Call the function - this should not raise any exceptions
        result = youtube_api.get_video_transcript(video_id)
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary contains the 'transcript' key
        assert result.get('transcript') is not None, "Result should contain 'transcript' key"
        
        # Verify the transcript value is a list
        assert isinstance(result.get('transcript'), list), "Transcript should be a list"
        
        # Verify the transcript list is not empty
        transcript = result.get('transcript')
        assert len(transcript) > 0, "Transcript list should not be empty"
        assert transcript, "Transcript list should be truthy (not empty)"


    def test_get_video_comments_success(self, youtube_api):
        """Test that get_video_comments works with a valid video ID and returns populated data"""
        video_id = "nUgGY18iTJw"
        
        # Call the function - this should not raise any exceptions
        result = youtube_api.get_video_comments(video_id)
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary contains the 'comments' key
        assert result.get('comments') is not None, "Result should contain 'comments' key"
        
        # Verify the comments value is a list
        assert isinstance(result.get('comments'), list), "Comments should be a list"
        
        # Verify the comments list is not empty
        comments = result.get('comments')
        assert len(comments) > 0, "Comments list should not be empty"
        assert comments, "Comments list should be truthy (not empty)"


    def test_search_success(self, youtube_api):
        """Test that search works with a valid search term and returns populated data"""
        search_term = "python is good"
        
        # Call the function - this should not raise any exceptions
        result = youtube_api.search(search_term)
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary contains the 'search_results' key
        assert result.get('search_results') is not None, "Result should contain 'search_results' key"
        
        # Verify the search_results value is a list
        assert isinstance(result.get('search_results'), list), "Search results should be a list"
        
        # Verify the search_results list is not empty
        search_results = result.get('search_results')
        assert len(search_results) > 0, "Search results list should not be empty"
        assert search_results, "Search results list should be truthy (not empty)"