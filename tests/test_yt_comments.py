import pytest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from yt_crawler import YoutubeAPI


class TestYoutubeAPIComments:
    """Tests for YouTube comments functionality"""
    
    @pytest.fixture
    def youtube_api(self):
        """Create a YoutubeAPI instance for testing"""
        return YoutubeAPI()


    def test_get_video_comments_success(self, youtube_api):
        """Test that get_video_comments works with a valid video ID and returns populated data"""
        video_id = "lH3ox-mE1xY"
        
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

    def test_get_video_comments_with_limit(self, youtube_api):
        """Test that get_video_comments respects the n_comments limit"""
        video_id = "v9ZApdKADxs"
        n_comments = 20
        
        # Call the function with n_comments limit
        result = youtube_api.get_video_comments(video_id, n_comments=n_comments)
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary contains the 'comments' key
        assert result.get('comments') is not None, "Result should contain 'comments' key"
        
        # Verify the comments value is a list
        comments = result.get('comments')
        assert isinstance(comments, list), "Comments should be a list"
        
        # Verify the comments list has exactly the requested number of items
        assert len(comments) == n_comments, f"Comments list should contain exactly {n_comments} items, got {len(comments)}"
        
        # Verify each comment is not None/empty
        assert all(comment is not None for comment in comments), "All comments should be non-None"


    def test_get_video_comments_with_none_limit(self, youtube_api):
        """Test that get_video_comments with n_comments=None returns all comments (same as no parameter)"""
        video_id = "v9ZApdKADxs"
        
        # Call the function with n_comments=None (explicit)
        result_with_none = youtube_api.get_video_comments(video_id, n_comments=None)
        
        # Call the function without n_comments parameter (implicit None)
        result_without_param = youtube_api.get_video_comments(video_id)
        
        # Verify both results are dictionaries
        assert isinstance(result_with_none, dict), "Result with None should be a dictionary"
        assert isinstance(result_without_param, dict), "Result without param should be a dictionary"
        
        # Verify both contain comments
        comments_with_none = result_with_none.get('comments')
        comments_without_param = result_without_param.get('comments')
        
        assert isinstance(comments_with_none, list), "Comments with None should be a list"
        assert isinstance(comments_without_param, list), "Comments without param should be a list"
        
        # Verify we got a reasonable number of comments (more than our test limit of 20)
        assert len(comments_with_none) > 20, \
            f"Should return more than 20 comments when fetching all, got {len(comments_with_none)}"


    def test_fetch_bulk_comments_structure_validation(self, youtube_api):
        """Test that get_video_comments returns 200 comments with correct structure for specific video"""
        video_id = "KTzcJgRxfiY"
        n_comments = 229
        expected_keys = ['key', 'properties', 'author', 'toolbar', 'avatar']
        
        # Call the function with n_comments limit
        result = youtube_api.get_video_comments(video_id, n_comments=n_comments)
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary contains the 'comments' key
        assert result.get('comments') is not None, "Result should contain 'comments' key"
        
        # Verify the comments value is a list
        comments = result.get('comments')
        assert isinstance(comments, list), "Comments should be a list"
        
        # Verify the comments list has exactly the requested number of items
        assert len(comments) == n_comments, f"Comments list should contain exactly {n_comments} items, got {len(comments)}"
        
        # Verify each comment is a dictionary
        assert all(isinstance(comment, dict) for comment in comments), "All comments should be dictionaries"
        
        # Verify each comment has all required keys
        assert all(
            all(key in comment for key in expected_keys) for comment in comments
        ), f"All comments should contain the keys: {expected_keys}"
        
        # Verify no comment is None or empty
        assert all(comment is not None for comment in comments), "All comments should be non-None"


    def test_get_video_comments_sort_by_top_comments(self, youtube_api):
        """Test that get_video_comments works with sort_by='top_comments'"""
        video_id = "lH3ox-mE1xY"
        expected_keys = ['key', 'properties', 'author', 'toolbar', 'avatar']
        
        # Call the function with explicit top_comments sorting
        result = youtube_api.get_video_comments(video_id, sort_by='top_comments')
        
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
        
        # Verify each comment is a dictionary
        assert all(isinstance(comment, dict) for comment in comments), "All comments should be dictionaries"
        
        # Verify each comment has all required keys
        assert all(
            all(key in comment for key in expected_keys) for comment in comments
        ), f"All comments should contain the keys: {expected_keys}"
        
        # Verify no comment is None or empty
        assert all(comment is not None for comment in comments), "All comments should be non-None"
        assert all(comment for comment in comments), "All comments should be non-empty"

    def test_get_video_comments_sort_by_newest(self, youtube_api):
        """Test that get_video_comments works with sort_by='newest'"""
        video_id = "v9ZApdKADxs"
        expected_keys = ['key', 'properties', 'author', 'toolbar', 'avatar']
        
        # Call the function with newest sorting
        result = youtube_api.get_video_comments(video_id, sort_by='newest')
        
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
        
        # Verify each comment is a dictionary
        assert all(isinstance(comment, dict) for comment in comments), "All comments should be dictionaries"
        
        # Verify each comment has all required keys
        assert all(
            all(key in comment for key in expected_keys) for comment in comments
        ), f"All comments should contain the keys: {expected_keys}"
        
        # Verify no comment is None or empty
        assert all(comment is not None for comment in comments), "All comments should be non-None"
        assert all(comment for comment in comments), "All comments should be non-empty"

    def test_get_video_comments_sort_by_with_limit(self, youtube_api):
        """Test that get_video_comments works with sort_by parameter combined with n_comments limit"""
        video_id = "KTzcJgRxfiY"
        n_comments = 15
        expected_keys = ['key', 'properties', 'author', 'toolbar', 'avatar']
        
        # Test with top_comments sorting and limit
        result_top = youtube_api.get_video_comments(video_id, n_comments=n_comments, sort_by='top_comments')
        
        # Verify the result structure for top_comments
        assert isinstance(result_top, dict), "Result should be a dictionary"
        assert result_top.get('comments') is not None, "Result should contain 'comments' key"
        
        comments_top = result_top.get('comments')
        assert isinstance(comments_top, list), "Comments should be a list"
        assert len(comments_top) == n_comments, f"Comments list should contain exactly {n_comments} items, got {len(comments_top)}"
        
        # Verify each comment structure for top_comments
        assert all(isinstance(comment, dict) for comment in comments_top), "All top comments should be dictionaries"
        assert all(
            all(key in comment for key in expected_keys) for comment in comments_top
        ), f"All top comments should contain the keys: {expected_keys}"
        assert all(comment is not None for comment in comments_top), "All top comments should be non-None"
        assert all(comment for comment in comments_top), "All top comments should be non-empty"
        
        # Test with newest sorting and limit
        result_newest = youtube_api.get_video_comments(video_id, n_comments=n_comments, sort_by='newest')
        
        # Verify the result structure for newest
        assert isinstance(result_newest, dict), "Result should be a dictionary"
        assert result_newest.get('comments') is not None, "Result should contain 'comments' key"
        
        comments_newest = result_newest.get('comments')
        assert isinstance(comments_newest, list), "Comments should be a list"
        assert len(comments_newest) == n_comments, f"Comments list should contain exactly {n_comments} items, got {len(comments_newest)}"
        
        # Verify each comment structure for newest
        assert all(isinstance(comment, dict) for comment in comments_newest), "All newest comments should be dictionaries"
        assert all(
            all(key in comment for key in expected_keys) for comment in comments_newest
        ), f"All newest comments should contain the keys: {expected_keys}"
        assert all(comment is not None for comment in comments_newest), "All newest comments should be non-None"
        assert all(comment for comment in comments_newest), "All newest comments should be non-empty"