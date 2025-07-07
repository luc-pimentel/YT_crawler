import pytest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from yt_crawler import YoutubeAPI


class TestSearchMaxParameter:
    """Tests for the new max parameter in YouTube search functionality"""
    
    @pytest.fixture
    def youtube_api(self) -> YoutubeAPI:
        """Create a YoutubeAPI instance for testing"""
        return YoutubeAPI()

    def test_search_with_max_parameter_basic(self, youtube_api: YoutubeAPI):
        """Test that search works with max parameter and returns correct number of results"""
        search_term = "python programming"
        max_results = 10
        
        # Call the function with max parameter
        result = youtube_api.search(search_term, max=max_results)
        
        # Verify the result structure
        assert isinstance(result, dict), "Result should be a dictionary"
        assert 'search_results' in result, "Result should contain 'search_results' key"
        
        # Verify the search_results value is a list
        search_results = result['search_results']
        assert isinstance(search_results, list), "Search results should be a list"
        
        # Verify we get exactly the requested number of results
        assert len(search_results) == max_results, f"Should return exactly {max_results} results, got {len(search_results)}"
        
        # Verify all results are valid video objects
        assert all(isinstance(video, dict) for video in search_results), "All search results should be dictionaries"
        assert all('videoId' in video for video in search_results), "All search results should contain 'videoId' key"
        assert all('title' in video for video in search_results), "All search results should contain 'title' key"

    def test_search_with_max_parameter_small_value(self, youtube_api: YoutubeAPI):
        """Test that search works with small max value (1 result)"""
        search_term = "python tutorial"
        max_results = 1
        
        # Call the function with max=1
        result = youtube_api.search(search_term, max=max_results)
        
        # Verify the result structure
        assert isinstance(result, dict), "Result should be a dictionary"
        assert 'search_results' in result, "Result should contain 'search_results' key"
        
        # Verify we get exactly 1 result
        search_results = result['search_results']
        assert len(search_results) == 1, f"Should return exactly 1 result, got {len(search_results)}"
        
        # Verify the single result is valid
        video = search_results[0]
        assert isinstance(video, dict), "Search result should be a dictionary"
        assert 'videoId' in video, "Search result should contain 'videoId' key"
        assert 'title' in video, "Search result should contain 'title' key"

    def test_search_with_max_parameter_medium_value(self, youtube_api: YoutubeAPI):
        """Test that search works with medium max value (25 results)"""
        search_term = "machine learning"
        max_results = 25
        
        # Call the function with max=25
        result = youtube_api.search(search_term, max=max_results)
        
        # Verify the result structure
        assert isinstance(result, dict), "Result should be a dictionary"
        assert 'search_results' in result, "Result should contain 'search_results' key"
        
        # Verify we get exactly the requested number of results
        search_results = result['search_results']
        assert len(search_results) == max_results, f"Should return exactly {max_results} results, got {len(search_results)}"
        
        # Verify all results are valid
        assert all(isinstance(video, dict) for video in search_results), "All search results should be dictionaries"
        assert all('videoId' in video for video in search_results), "All search results should contain 'videoId' key"

    def test_search_backward_compatibility_n_videos_still_works(self, youtube_api: YoutubeAPI):
        """Test that the old n_videos parameter still works for backward compatibility"""
        search_term = "web development"
        n_videos = 15
        
        # Call the function with old n_videos parameter (no max specified)
        result = youtube_api.search(search_term, n_videos=n_videos)
        
        # Verify the result structure
        assert isinstance(result, dict), "Result should be a dictionary"
        assert 'search_results' in result, "Result should contain 'search_results' key"
        
        # Verify we get exactly the requested number of results
        search_results = result['search_results']
        assert len(search_results) == n_videos, f"Should return exactly {n_videos} results, got {len(search_results)}"
        
        # Verify all results are valid
        assert all(isinstance(video, dict) for video in search_results), "All search results should be dictionaries"
        assert all('videoId' in video for video in search_results), "All search results should contain 'videoId' key"

    def test_search_max_parameter_takes_precedence_over_n_videos(self, youtube_api: YoutubeAPI):
        """Test that max parameter takes precedence over n_videos when both are specified"""
        search_term = "data science"
        n_videos = 20
        max_results = 5
        
        # Call the function with both parameters - max should take precedence
        result = youtube_api.search(search_term, n_videos=n_videos, max=max_results)
        
        # Verify the result structure
        assert isinstance(result, dict), "Result should be a dictionary"
        assert 'search_results' in result, "Result should contain 'search_results' key"
        
        # Verify we get the max number of results (not n_videos)
        search_results = result['search_results']
        assert len(search_results) == max_results, f"Should return exactly {max_results} results (max takes precedence), got {len(search_results)}"
        
        # Verify all results are valid
        assert all(isinstance(video, dict) for video in search_results), "All search results should be dictionaries"
        assert all('videoId' in video for video in search_results), "All search results should contain 'videoId' key"

    def test_search_with_max_parameter_and_filters(self, youtube_api: YoutubeAPI):
        """Test that max parameter works correctly with other filters"""
        search_term = "python"
        max_results = 8
        duration = "under_4_minutes"
        
        # Call the function with max parameter and duration filter
        result = youtube_api.search(search_term, max=max_results, duration=duration)
        
        # Verify the result structure
        assert isinstance(result, dict), "Result should be a dictionary"
        assert 'search_results' in result, "Result should contain 'search_results' key"
        
        # Verify we get exactly the requested number of results
        search_results = result['search_results']
        assert len(search_results) == max_results, f"Should return exactly {max_results} results with filters, got {len(search_results)}"
        
        # Verify all results are valid
        assert all(isinstance(video, dict) for video in search_results), "All search results should be dictionaries"
        assert all('videoId' in video for video in search_results), "All search results should contain 'videoId' key"
        assert all('title' in video for video in search_results), "All search results should contain 'title' key"