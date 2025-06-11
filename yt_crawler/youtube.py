import requests
from bs4 import BeautifulSoup
import json
from .utils import *
from .youtube_search import SearchMixin
from .youtube_comments import CommentsMixin
from .youtube_transcript import TranscriptMixin


class YoutubeAPI(SearchMixin, CommentsMixin, TranscriptMixin):

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
    

    def get_trending_videos(self):
        """
        Scrapes YouTube trending videos and returns them in a structured format.
        
        Returns:
            dict: Dictionary containing trending videos list
        """
        url = "https://www.youtube.com/feed/trending"
        raw_search_json = extract_youtube_initial_data(url, 'ytInitialData')
        
        try:
            two_column_browse_results_renderer = raw_search_json.get('contents').get('twoColumnBrowseResultsRenderer')
            contents = two_column_browse_results_renderer.get('tabs')[0].get('tabRenderer').get('content').get('sectionListRenderer').get('contents')
        except (AttributeError, IndexError, TypeError):
            raise Exception("Could not parse trending videos structure")
        
        videos_list = []
        
        for content in contents:
            try:
                section_renderer = content.get('itemSectionRenderer').get('contents')[0]
                reel_renderer = section_renderer.get('reelShelfRenderer')
                
                if reel_renderer:
                    videos = section_renderer.get('reelShelfRenderer').get('items')
                else:
                    shelf_renderer = section_renderer.get('shelfRenderer').get('content')
                    videos = shelf_renderer.get('expandedShelfContentsRenderer').get('items')
                
                videos_list.extend([video for video in videos if any(key in video for key in ['videoRenderer', 'shortsLockupViewModel'])])
            except (AttributeError, TypeError):
                # Skip sections that don't match expected structure
                continue
        
        return {'trending': videos_list}
    

    def get_trending_news(self):
        """
        Scrapes YouTube's trending news page and returns trending video data.
        
        Returns:
            dict: A dictionary containing trending news sections
        """
        url = "https://www.youtube.com/feed/news_destination"
        initial_data_response_json = extract_youtube_initial_data(url, 'ytInitialData')
        
        try:
            tabs = initial_data_response_json.get('contents').get('twoColumnBrowseResultsRenderer').get('tabs')
            tab_contents = tabs[0].get('tabRenderer').get('content').get('richGridRenderer').get('contents')
            trending_sections = [tab_content.get('richSectionRenderer').get('content').get('richShelfRenderer') for tab_content in tab_contents]
        except (AttributeError, IndexError, TypeError):
            raise Exception("Could not parse trending news structure")
        
        return {'trending_news': trending_sections}