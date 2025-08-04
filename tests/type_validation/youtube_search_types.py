import pytest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from yt_crawler import YoutubeAPI
from yt_crawler.types.search import SearchResultsModel, SearchResult
from pydantic import ValidationError


class TestYouTubeSearchTypes:
    """Tests for YouTube search types validation against real YouTube API data"""
    
    @pytest.fixture
    def youtube_api(self) -> YoutubeAPI:
        """Create a YoutubeAPI instance for testing"""
        return YoutubeAPI()

    def test_search_results_model_validation_basic(self, youtube_api: YoutubeAPI):
        """Test that real search results conform to SearchResultsModel"""
        search_term = "Praise jah in the moonlight"
        
        # Get real search results from API
        api_result = youtube_api.search(search_term, n_videos=5)
        
        # Verify API returned expected structure
        assert isinstance(api_result, dict), "API should return a dictionary"
        assert 'search_results' in api_result, "API result should contain 'search_results' key"
        assert isinstance(api_result['search_results'], list), "search_results should be a list"
        assert len(api_result['search_results']) > 0, "Should have at least one search result"
        
        # Test Pydantic model validation
        try:
            # Try Pydantic v2 first, fallback to v1
            try:
                validated_model = SearchResultsModel.model_validate(api_result)
                print("Using Pydantic v2 for validation")
            except AttributeError:
                validated_model = SearchResultsModel.parse_obj(api_result)
                print("Using Pydantic v1 for validation")
            
            # Verify the validated model
            assert isinstance(validated_model, SearchResultsModel), "Should create valid SearchResultsModel instance"
            assert len(validated_model.search_results) > 0, "Validated model should have search results"
            assert len(validated_model.search_results) == len(api_result['search_results']), "Validated model should have same number of results as API"
            
        except ValidationError as e:
            pytest.fail(f"Pydantic validation failed: {str(e)}")
        except Exception as e:
            pytest.fail(f"Unexpected error during validation: {str(e)}")

    def test_individual_search_result_validation(self, youtube_api: YoutubeAPI):
        """Test that individual search result items conform to SearchResult model"""
        search_term = "python programming"
        
        # Get real search results from API
        api_result = youtube_api.search(search_term, n_videos=3)
        search_results = api_result['search_results']
        
        # Test validation of individual search result items
        for i, search_result_data in enumerate(search_results):
            try:
                # Try Pydantic v2 first, fallback to v1
                try:
                    validated_result = SearchResult.model_validate(search_result_data)
                except AttributeError:
                    validated_result = SearchResult.parse_obj(search_result_data)
                
                # Verify basic properties exist
                assert validated_result.videoId, f"Search result {i} should have a videoId"
                assert validated_result.title, f"Search result {i} should have a title"
                assert validated_result.thumbnail, f"Search result {i} should have thumbnail data"
                # Note: lengthText is optional for live streams
                assert validated_result.viewCountText, f"Search result {i} should have view count text"
                
            except ValidationError as e:
                pytest.fail(f"Validation failed for search result {i}: {str(e)}")
            except Exception as e:
                pytest.fail(f"Unexpected error validating search result {i}: {str(e)}")

    def test_model_validation_with_different_search_terms(self, youtube_api: YoutubeAPI):
        """Test model validation with different search terms to ensure robustness"""
        test_search_terms = [
            "music",
            "tutorial",
            "news",
        ]
        
        for search_term in test_search_terms:
            try:
                # Get real search results from API
                api_result = youtube_api.search(search_term, n_videos=2)
                
                # Test Pydantic model validation
                try:
                    validated_model = SearchResultsModel.model_validate(api_result)
                except AttributeError:
                    validated_model = SearchResultsModel.parse_obj(api_result)
                
                # Basic verification
                assert len(validated_model.search_results) > 0, f"Should have results for search term: {search_term}"
                
            except ValidationError as e:
                pytest.fail(f"Validation failed for search term '{search_term}': {str(e)}")
            except Exception as e:
                pytest.fail(f"Unexpected error for search term '{search_term}': {str(e)}")

    def test_model_validation_required_fields(self, youtube_api: YoutubeAPI):
        """Test that all required fields are present in real API data"""
        search_term = "test"
        
        # Get real search results from API
        api_result = youtube_api.search(search_term, n_videos=1)
        
        if api_result['search_results']:
            first_result = api_result['search_results'][0]
            
            # Check that key required fields exist in the raw API data
            required_fields = [
                'videoId', 'thumbnail', 'title', 'longBylineText', 
                'lengthText', 'viewCountText', 'navigationEndpoint',
                'ownerText', 'shortBylineText', 'trackingParams',
                'showActionMenu', 'shortViewCountText', 'menu',
                'channelThumbnailSupportedRenderers', 'thumbnailOverlays',
                'searchVideoResultEntityKey'
            ]
            
            for field in required_fields:
                assert field in first_result, f"Required field '{field}' missing from API response"
            
            # Validate with Pydantic
            try:
                try:
                    SearchResult.model_validate(first_result)
                except AttributeError:
                    SearchResult.parse_obj(first_result)
            except ValidationError as e:
                pytest.fail(f"Required field validation failed: {str(e)}")