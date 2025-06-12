import requests
from bs4 import BeautifulSoup
import json
from .utils import *
from .youtube_search import SearchMixin
from .youtube_comments import CommentsMixin
from .youtube_transcript import TranscriptMixin
from .youtube_news import NewsMixin
from .youtube_trending import TrendingMixin


class YoutubeAPI(SearchMixin, CommentsMixin, TranscriptMixin, NewsMixin, TrendingMixin):

    def get_video_details(self, video_id):
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

        video_details = initial_player_response_json.get('videoDetails')

        if not video_details:
            raise Exception("No video details found")
        
        return video_details