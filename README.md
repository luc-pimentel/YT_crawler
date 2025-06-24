# YT_crawler

A comprehensive Python library for crawling and extracting data from YouTube without using the official YouTube API. This library provides functionality to search videos, extract video details, fetch comments, get transcripts, and monitor trending content.

## Features

- **Video Search**: Search YouTube videos with advanced filtering options (upload date, duration, features, sorting)
- **Video Details**: Extract comprehensive video metadata including views, likes, description, and channel information
- **Comments Extraction**: Fetch video comments with threading support
- **Transcripts**: Get video transcripts/captions when available
- **Trending Videos**: Monitor and extract trending videos from different regions
- **News Content**: Extract YouTube news and current events content
- **No API Key Required**: Works without YouTube API quotas or restrictions

## Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/luc-pimentel/YT_crawler.git
cd YT_crawler
pip install -r requirements.txt
```

## Quick Start

```python
from yt_crawler import YouTube

# Initialize the crawler
yt = YouTube()

# Search for videos
search_results = yt.search("python programming", n_videos=50)

# Get video details
video_details = yt.get_video_details("VIDEO_ID_HERE")

# Get video comments
comments = yt.get_comments("VIDEO_ID_HERE", n_comments=100)

# Get trending videos
trending = yt.get_trending_videos(region='US')
```

## Core Components

### SearchMixin (`youtube_search.py`)

Provides advanced YouTube search functionality with filtering options:

- **Upload Date**: `last_hour`, `today`, `this_week`, `this_month`, `this_year`
- **Duration**: `under_4_minutes`, `4_20_minutes`, `over_20_minutes`
- **Features**: `live`, `4k`, `hd`, `subtitles_cc`, `creative_commons`, `360`, `vr180`, `3d`, `hdr`, `location`, `purchased`
- **Sort By**: `relevance`, `upload_date`, `view_count`, `rating`

```python
# Search with filters
results = yt.search(
    search_term="machine learning",
    n_videos=100,
    upload_date="this_week",
    duration="over_20_minutes",
    features="hd",
    sort_by="view_count"
)
```

### Video Details (`youtube.py`)

Extract comprehensive video information including:
- Title, description, view count
- Like/dislike ratios
- Channel information
- Upload date and duration
- Video quality options

### Comments (`youtube_comments.py`)

Fetch video comments with support for:
- Threaded replies
- Comment metadata (likes, author, timestamp)
- Pagination for large comment sections

### Transcripts (`youtube_transcript.py`)

Extract video transcripts and captions:
- Multiple language support
- Automatic and manual captions
- Timestamp information

### Trending (`youtube_trending.py`)

Monitor trending content:
- Region-specific trending
- Category filtering
- Real-time trending data

### News (`youtube_news.py`)

Extract news and current events content from YouTube's news section.

## Configuration

The library uses configuration settings in `config.py`:

```python
# Custom headers for requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    # ... other headers
}
```

## Error Handling

The library includes custom exceptions in `exceptions.py` for better error handling:

- Network-related errors
- Parsing errors
- Rate limiting handling
- Invalid video ID errors

## Utilities

The `utils.py` module provides helper functions for:
- JSON extraction from HTML scripts
- Data parsing and cleaning
- Request handling and retries
- YouTube URL processing

## Testing

Run the test suite to ensure everything works correctly:

```bash
python -m pytest tests/
```

Test files include:
- `test_yt_search.py` - Search functionality tests
- `test_yt_video_details.py` - Video details extraction tests
- `test_yt_comments.py` - Comments extraction tests
- `test_yt_transcript.py` - Transcript extraction tests
- `test_yt_trending.py` - Trending videos tests
- `test_yt_news.py` - News content tests
- `test_utils.py` - Utility functions tests

## Rate Limiting and Best Practices

- Use reasonable delays between requests for large-scale crawling
- Respect YouTube's terms of service

## Examples

### Advanced Search with Multiple Filters

```python
# Search for recent HD programming tutorials
results = yt.search(
    search_term="python tutorial",
    n_videos=50,
    upload_date="this_month",
    duration="over_20_minutes",
    features="hd",
    sort_by="view_count"
)

for video in results['search_results']:
    print(f"Title: {video.get('title', {}).get('runs', [{}])[0].get('text', 'N/A')}")
    print(f"Views: {video.get('viewCountText', {}).get('simpleText', 'N/A')}")
```

### Batch Video Processing

```python
video_ids = ["VIDEO_ID_1", "VIDEO_ID_2", "VIDEO_ID_3"]

for video_id in video_ids:
    try:
        details = yt.get_video_details(video_id)
        comments = yt.get_comments(video_id, n_comments=50)
        transcript = yt.get_transcript(video_id)
        
        # Process the data
        print(f"Processed: {details.get('title', 'Unknown')}")
        
    except Exception as e:
        print(f"Error processing {video_id}: {e}")
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This library is for educational and research purposes. Please respect YouTube's terms of service and use responsibly. The library does not use official YouTube APIs and relies on web scraping, which may be subject to changes in YouTube's website structure.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.