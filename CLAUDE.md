# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

YT_crawler is a comprehensive Python library for extracting data from YouTube without using the official YouTube API. It provides functionality to search videos, extract video details, fetch comments, get transcripts, and monitor trending content through web scraping.

## Architecture

The project follows a mixin-based architecture with a main `YoutubeAPI` class that inherits from multiple specialized mixins:

- **YoutubeAPI** (`yt_crawler/youtube.py`): Main API class that combines all mixins and provides `get_video_details()`
- **SearchMixin** (`yt_crawler/youtube_search.py`): Advanced search functionality with filtering
- **CommentsMixin** (`yt_crawler/youtube_comments.py`): Video comments extraction with threading support
- **TranscriptMixin** (`yt_crawler/youtube_transcript.py`): Video transcript/caption extraction
- **NewsMixin** (`yt_crawler/youtube_news.py`): YouTube news content extraction
- **TrendingMixin** (`yt_crawler/youtube_trending.py`): Trending videos monitoring

### Core Components

- **Types System** (`yt_crawler/types/`): Comprehensive Pydantic models for type validation
  - `search.py`: Search result models
  - `comments.py`: Comment structure models
  - `video_details.py`: Video metadata models
  - `trending_news.py`: News content models
  - All models provide strict validation for YouTube API responses

- **Utilities** (`yt_crawler/utils.py`): Helper functions for JSON extraction, HTML parsing, and request handling
- **Configuration** (`yt_crawler/config.py`): Headers and request configuration
- **Exceptions** (`yt_crawler/exceptions.py`): Custom error handling

## Development Commands

### Testing
```bash
# Run all tests
python -m pytest tests/

# Run specific test module
python -m pytest tests/test_yt_search.py
python -m pytest tests/test_yt_comments.py
python -m pytest tests/test_yt_video_details.py

# Run type validation tests (uses real API calls)
python -m pytest tests/type_validation/

# Run individual test
python -m pytest tests/test_utils.py::TestExtractYoutubePageScripts::test_extract_youtube_page_scripts_with_headers
```

### Code Quality
The project uses pytest for testing. Based on .gitignore, it supports:
- mypy (static type checking)
- ruff (linting and formatting)
- pytest (testing framework)

## Usage Patterns

### Basic Usage
```python
from yt_crawler import YoutubeAPI

yt = YoutubeAPI()

# Search with filters
results = yt.search("python programming", n_videos=50, 
                   upload_date="this_week", duration="over_20_minutes")

# Get video details  
details = yt.get_video_details("VIDEO_ID")

# Get comments
comments = yt.get_comments("VIDEO_ID", n_comments=100)
```

### Search Filters
- **Upload Date**: `last_hour`, `today`, `this_week`, `this_month`, `this_year`
- **Duration**: `under_4_minutes`, `4_20_minutes`, `over_20_minutes`  
- **Features**: `live`, `4k`, `hd`, `subtitles_cc`, `creative_commons`, `360`, `vr180`, `3d`, `hdr`
- **Sort By**: `relevance`, `upload_date`, `view_count`, `rating`

## Important Notes

- **No API Key Required**: Uses web scraping instead of official YouTube API
- **Rate Limiting**: Implement delays for large-scale crawling to respect YouTube's servers
- **Type Safety**: All responses are validated through Pydantic models
- **Error Handling**: Custom exceptions in `exceptions.py` for different failure scenarios
- **Real API Testing**: Type validation tests make actual API calls to ensure models stay current

## File Structure Key Points

- Main API entry point: `yt_crawler/__init__.py` exports `YoutubeAPI`
- All mixins are combined in the main `YoutubeAPI` class
- Comprehensive test coverage including real API validation
- Type definitions provide strict contracts for all YouTube data structures