# YouTube Data Hoarder Project Documentation

## Project Structure

### Types Directory (`yt_crawler/types/`)
Contains Pydantic models for data validation and type safety:

- **`search.py`**: Comprehensive Pydantic models for YouTube search results
  - `SearchResultsModel`: Main container for search results
  - `SearchResult`: Individual video search result with all metadata
  - `ThumbnailInfo`, `Thumbnail`: Video thumbnail data structures
  - `TextWithRuns`, `SimpleText`: Text content with formatting and accessibility
  - `NavigationEndpoint`, `WatchEndpoint`: Navigation and playback endpoints
  - All models include proper field validation, aliases, and documentation

- **`video_details.py`**: Pydantic models for YouTube video details API responses
  - `VideoDetailsResponse`: Main container for video details response
  - `VideoDetails`: Core video metadata (title, duration, view count, etc.)
  - `PlayerMicroformatRenderer`: Video microformat data
  - Models handle field aliases for camelCase to snake_case conversion
  - Includes proper validation for URLs, dates, and optional fields

### Test Validation Directory (`tests/type_validation/`)
Contains comprehensive test suites for Pydantic model validation:

- **`test_search_results_validation.py`**: Tests for search results models
  - Validates against real JSON data from `search_results.json`
  - Tests model structure, thumbnail validation, text runs
  - Includes error handling and edge case testing
  - Uses pytest fixtures for sample data loading

- **`test_video_details_validation.py`**: Tests for video details models
  - Validates against real YouTube API data
  - Tests VideoDetailsResponse, microformat validation
  - Includes field alias testing and optional field handling
  - Uses live API calls with fallback to skip if unavailable

## Usage Notes

### Running Type Validation Tests
```bash
# Run all type validation tests
pytest tests/type_validation/

# Run specific test files
pytest tests/type_validation/test_search_results_validation.py
pytest tests/type_validation/test_video_details_validation.py
```

### Using Pydantic Models
```python
from yt_crawler.types.search import SearchResultsModel
from yt_crawler.types.video_details import VideoDetailsResponse

# Validate search results data
search_data = SearchResultsModel.model_validate(json_data)

# Validate video details data  
video_data = VideoDetailsResponse.model_validate(api_response)
```

### Model Features
- **Field Validation**: All models include proper type checking and validation
- **Field Aliases**: Automatic conversion between camelCase and snake_case
- **Documentation**: Comprehensive field descriptions and model documentation
- **Optional Fields**: Proper handling of optional/nullable fields
- **URL Validation**: HTTP/HTTPS URL validation using Pydantic's HttpUrl type
- **Error Handling**: Comprehensive validation error reporting