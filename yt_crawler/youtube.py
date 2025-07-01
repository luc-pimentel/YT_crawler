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
        # Get the webpage content
        url = f"https://www.youtube.com/watch?v={video_id}"
        scripts = extract_youtube_page_scripts(url, headers=HEADERS)
        
        video_details_dict = grab_dict_by_key(scripts, 'videoDetails')
        if not video_details_dict:
            raise Exception("No video details found")
        
        video_details_key_data = video_details_dict.get('videoDetails')
        microformat_key_data = video_details_dict.get('microformat')

        # Wrap both in video_details dictionary
        video_details = {
            'videoDetails': video_details_key_data,
            'microformat': microformat_key_data
        }
        
        return video_details