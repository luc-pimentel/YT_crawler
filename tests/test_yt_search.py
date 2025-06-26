import pytest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from yt_crawler import YoutubeAPI


class TestYoutubeSearch:
    """Tests for YouTube search functionality"""
    
    @pytest.fixture
    def youtube_api(self):
        """Create a YoutubeAPI instance for testing"""
        return YoutubeAPI()

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
        search_results = result.get('search_results', [])
        assert len(search_results) > 0, "Search results list should not be empty"
        assert search_results, "Search results list should be truthy (not empty)"

    def test_search_result_item_structure(self, youtube_api):
        """Test that each search result item has the required keys"""
        search_term = "python is good"
        
        # Call the function - this should not raise any exceptions
        result = youtube_api.search(search_term)
        
        # Get the search results list
        search_results = result.get('search_results')
        
        # Ensure we have results to test
        assert search_results, "Search results should not be empty for structure testing"
        
        # Test that all items are dictionaries
        assert all(isinstance(item, dict) for item in search_results), "All search result items should be dictionaries"
        
        # Test that all items have the required keys
        assert all('videoId' in item for item in search_results), "All search result items should contain 'videoId' key"
        assert all('thumbnail' in item for item in search_results), "All search result items should contain 'thumbnail' key"
        assert all('title' in item for item in search_results), "All search result items should contain 'title' key"


    def test_search_large_n_videos(self, youtube_api):
        """Test that search works with a large n_videos count and returns exactly that many videos"""
        search_term = "python is good"
        n_videos = 167
        
        # Call the function with large n_videos count
        result = youtube_api.search(search_term, n_videos=n_videos)
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary contains the 'search_results' key
        assert result.get('search_results') is not None, "Result should contain 'search_results' key"
        
        # Verify the search_results value is a list
        search_results = result.get('search_results')
        assert isinstance(search_results, list), "Search results should be a list"
        
        # Verify we get exactly the requested number of videos
        assert len(search_results) == n_videos, f"Should return exactly {n_videos} videos, got {len(search_results)}"
        
        # Verify all results are valid video objects (not None)
        assert all(video is not None for video in search_results), "All search results should be valid (not None)"
        
        # Verify basic structure is maintained for large result sets
        assert all(isinstance(video, dict) for video in search_results), "All search result items should be dictionaries"
        assert all('videoId' in video for video in search_results), "All search result items should contain 'videoId' key"
        assert all('thumbnail' in video for video in search_results), "All search result items should contain 'thumbnail' key"
        assert all('title' in video for video in search_results), "All search result items should contain 'title' key"


    def test_search_with_sorting(self, youtube_api):
        """Test that search works with sorting parameter (upload_date)"""
        search_term = "python is good"
        sort_by = "upload_date"
        n_videos = 10
        
        # Call the function with sorting parameter
        result = youtube_api.search(search_term, n_videos=n_videos, sort_by=sort_by)
        
        # Verify the result structure is maintained
        assert isinstance(result, dict), "Result should be a dictionary"
        assert result.get('search_results') is not None, "Result should contain 'search_results' key"
        
        # Verify the search_results value is a list
        search_results = result.get('search_results')
        assert isinstance(search_results, list), "Search results should be a list"
        
        # Verify we get the requested number of videos
        assert len(search_results) == n_videos, f"Should return exactly {n_videos} videos, got {len(search_results)}"
        
        # Verify all results are valid video objects with required structure
        assert all(isinstance(video, dict) for video in search_results), "All search result items should be dictionaries"
        assert all('videoId' in video for video in search_results), "All search result items should contain 'videoId' key"
        assert all('thumbnail' in video for video in search_results), "All search result items should contain 'thumbnail' key"
        assert all('title' in video for video in search_results), "All search result items should contain 'title' key"


    def test_search_with_sorting_large_n_videos(self, youtube_api):
        """Test that search works with sorting parameter and large n_videos count"""
        search_term = "python is good"
        sort_by = "upload_date"
        n_videos = 127
        
        # Call the function with sorting parameter and large n_videos count
        result = youtube_api.search(search_term, n_videos=n_videos, sort_by=sort_by)
        
        # Verify the result structure is maintained
        assert isinstance(result, dict), "Result should be a dictionary"
        assert result.get('search_results') is not None, "Result should contain 'search_results' key"
        
        # Verify the search_results value is a list
        search_results = result.get('search_results')
        assert isinstance(search_results, list), "Search results should be a list"
        
        # Verify we get exactly the requested number of videos
        assert len(search_results) == n_videos, f"Should return exactly {n_videos} videos, got {len(search_results)}"
        
        # Verify all results are valid video objects (not None)
        assert all(video is not None for video in search_results), "All search results should be valid (not None)"
        
        # Verify basic structure is maintained for large result sets with sorting
        assert all(isinstance(video, dict) for video in search_results), "All search result items should be dictionaries"
        assert all('videoId' in video for video in search_results), "All search result items should contain 'videoId' key"
        assert all('thumbnail' in video for video in search_results), "All search result items should contain 'thumbnail' key"
        assert all('title' in video for video in search_results), "All search result items should contain 'title' key"


    def test_search_with_upload_date_filter(self, youtube_api):
        """Test that search works with upload_date filter (last_hour)"""
        search_term = "python is good"
        upload_date = "today"
        n_videos = 10
        
        # Call the function with upload_date filter
        result = youtube_api.search(search_term, n_videos=n_videos, upload_date=upload_date)
        
        # Verify the result structure is maintained
        assert isinstance(result, dict), "Result should be a dictionary"
        assert result.get('search_results') is not None, "Result should contain 'search_results' key"
        
        # Verify the search_results value is a list
        search_results = result.get('search_results')
        assert isinstance(search_results, list), "Search results should be a list"
        
        # Verify we get the requested number of videos (or less if not enough recent videos)
        assert len(search_results) <= n_videos, f"Should return at most {n_videos} videos, got {len(search_results)}"
        
        # Verify all results are valid video objects with required structure
        if search_results:  # Only check structure if we have results
            assert all(isinstance(video, dict) for video in search_results), "All search result items should be dictionaries"
            assert all('videoId' in video for video in search_results), "All search result items should contain 'videoId' key"
            assert all('thumbnail' in video for video in search_results), "All search result items should contain 'thumbnail' key"
            assert all('title' in video for video in search_results), "All search result items should contain 'title' key"


    def test_search_with_duration_filter(self, youtube_api):
        """Test that search works with duration filter (under_4_minutes)"""
        search_term = "python is good"
        duration = "under_4_minutes"
        n_videos = 10
        
        # Call the function with duration filter
        result = youtube_api.search(search_term, n_videos=n_videos, duration=duration)
        
        # Verify the result structure is maintained
        assert isinstance(result, dict), "Result should be a dictionary"
        assert result.get('search_results') is not None, "Result should contain 'search_results' key"
        
        # Verify the search_results value is a list
        search_results = result.get('search_results')
        assert isinstance(search_results, list), "Search results should be a list"
        
        # Verify we get the requested number of videos
        assert len(search_results) == n_videos, f"Should return exactly {n_videos} videos, got {len(search_results)}"
        
        # Verify all results are valid video objects with required structure
        assert all(isinstance(video, dict) for video in search_results), "All search result items should be dictionaries"
        assert all('videoId' in video for video in search_results), "All search result items should contain 'videoId' key"
        assert all('thumbnail' in video for video in search_results), "All search result items should contain 'thumbnail' key"
        assert all('title' in video for video in search_results), "All search result items should contain 'title' key"


    def test_search_with_features_filter(self, youtube_api):
        """Test that search works with features filter (hd)"""
        search_term = "python is good"
        features = "hd"
        n_videos = 10
        
        # Call the function with features filter
        result = youtube_api.search(search_term, n_videos=n_videos, features=features)
        
        # Verify the result structure is maintained
        assert isinstance(result, dict), "Result should be a dictionary"
        assert result.get('search_results') is not None, "Result should contain 'search_results' key"
        
        # Verify the search_results value is a list
        search_results = result.get('search_results')
        assert isinstance(search_results, list), "Search results should be a list"
        
        # Verify we get the requested number of videos
        assert len(search_results) == n_videos, f"Should return exactly {n_videos} videos, got {len(search_results)}"
        
        # Verify all results are valid video objects with required structure
        assert all(isinstance(video, dict) for video in search_results), "All search result items should be dictionaries"
        assert all('videoId' in video for video in search_results), "All search result items should contain 'videoId' key"
        assert all('thumbnail' in video for video in search_results), "All search result items should contain 'thumbnail' key"
        assert all('title' in video for video in search_results), "All search result items should contain 'title' key"


    def test_search_with_three_filters_combination(self, youtube_api):
        """Test that search works with four filters combined (duration + features + upload_date)"""
        search_term = "python tutorial"
        duration = "4_20_minutes"
        features = "hd"
        upload_date = "this_week"
        n_videos = 8
        
        # Call the function with four filters
        result = youtube_api.search(
            search_term, 
            n_videos=n_videos, 
            duration=duration,
            features=features,
            upload_date=upload_date
        )
        
        # Verify the result structure is maintained
        assert isinstance(result, dict), "Result should be a dictionary"
        assert result.get('search_results') is not None, "Result should contain 'search_results' key"
        
        # Verify the search_results value is a list
        search_results = result.get('search_results')
        assert isinstance(search_results, list), "Search results should be a list"
        
        # Verify we get some results (filters might be restrictive, so allow for fewer results)
        assert len(search_results) <= n_videos, f"Should return at most {n_videos} videos, got {len(search_results)}"
        
        # If we have results, verify their structure
        assert all(isinstance(video, dict) for video in search_results), "All search result items should be dictionaries"
        assert all('videoId' in video for video in search_results), "All search result items should contain 'videoId' key"
        assert all('thumbnail' in video for video in search_results), "All search result items should contain 'thumbnail' key"
        assert all('title' in video for video in search_results), "All search result items should contain 'title' key"