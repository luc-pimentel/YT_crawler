from .utils import *
from .youtube_search import SearchMixin
from .youtube_comments import CommentsMixin
from .youtube_transcript import TranscriptMixin
from .youtube_news import NewsMixin
from .youtube_trending import TrendingMixin
from typing import Any

class YoutubeAPI(SearchMixin, CommentsMixin, TranscriptMixin, NewsMixin, TrendingMixin):

    def get_video_details(self, video_id: str) -> dict[str, Any]:
        """
        Get video details from YouTube video ID
        
        Args:
            video_id (str): YouTube video ID
            
        Returns:
            dict: Video details including title, description, view count etc.
        """
        # Construct YouTube URL
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Get the webpage content
        initial_player_response_json = extract_youtube_initial_data(youtube_url, 'ytInitialPlayerResponse')
        if not initial_player_response_json:
            raise Exception("Could not find initial player response JSON")
        
        # Extract both videoDetails and microformat
        video_details_data = initial_player_response_json.get('videoDetails', {})
        microformat_data = initial_player_response_json.get('microformat', {})

        if not video_details_data :
            raise Exception("No video details found")
        if not microformat_data:
            raise Exception("No microformat data found")

        # Wrap both in video_details dictionary
        video_details = {
            'videoDetails': video_details_data,
            'microformat': microformat_data
        }
        
        return video_details