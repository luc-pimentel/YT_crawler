import requests
from bs4 import BeautifulSoup
import json
from .utils import *
from .config import HEADERS


class YoutubeAPI:

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
    

    def get_video_transcript(self, video_id):
        """
            Get video transcript from YouTube video ID
            
            Args:
                video_id (str): YouTube video ID
                
            Returns:
                dict: Video transcript
        """
            # Construct YouTube URL
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
            
            # Get the webpage content
        initial_player_response_json = extract_youtube_initial_data(youtube_url, 'ytInitialPlayerResponse')

        captions_element = initial_player_response_json.get('captions')

        if not captions_element:
            raise Exception("Video has no transcript available")

        caption_url = captions_element.get('playerCaptionsTracklistRenderer').get('captionTracks')[0].get('baseUrl')
        caption_request = requests.get(caption_url)
        video_transcript = xml_transcript_to_json_bs4(caption_request.text)

        return video_transcript
    

    def get_video_comments(self, video_id):
        """
        Get video comments from YouTube video ID
            
        Args:
            video_id (str): YouTube video ID
                
        Returns:
            dict: Video comments data
        """
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        initial_data_response_json = extract_youtube_initial_data(youtube_url, 'ytInitialData')

        try:
            comment_section_renderer_json = initial_data_response_json.get('engagementPanels')[0].get('engagementPanelSectionListRenderer').get('content').get('sectionListRenderer').get('contents')[0]
            continuation_endpoint = comment_section_renderer_json.get('itemSectionRenderer').get('contents')[0].get('continuationItemRenderer').get('continuationEndpoint')
            click_tracking_params = continuation_endpoint.get('clickTrackingParams')
            continuation_token = continuation_endpoint.get('continuationCommand').get('token')
        except (AttributeError, IndexError, TypeError):
            raise Exception("Could not find comment continuation data")

        data = fetch_youtube_comments_data(continuation_token, click_tracking_params)

        try:
            mutations_list = data.get('frameworkUpdates').get('entityBatchUpdate').get('mutations')
            comments = [mutation.get('payload').get('commentEntityPayload') for mutation in mutations_list if 'commentEntityPayload' in mutation.get('payload').keys()]
        except (AttributeError, TypeError):
            raise Exception("Could not parse comment data from response")

        comments_json = {'comments': comments}
        return comments_json
    

    def search(self, search_term):
        """
        Search YouTube videos
        
        Args:
            search_term (str): Search query
            
        Returns:
            dict: Search results
        """
        # URL encode the search term to handle spaces and special characters
        quoted_search_term = requests.utils.quote(search_term)
        url = f"https://www.youtube.com/results?search_query={quoted_search_term}"
        
        raw_search_json = extract_youtube_initial_data(url, 'ytInitialData')
        
        try:
            search_contents = raw_search_json.get('contents').get('twoColumnSearchResultsRenderer').get('primaryContents').get('sectionListRenderer').get('contents')
            item_section_renderer_contents = search_contents[0].get('itemSectionRenderer').get('contents')
            videos = [video.get('videoRenderer') for video in item_section_renderer_contents if video.get('videoRenderer')]
        except (AttributeError, IndexError, TypeError):
            raise Exception("Could not parse search results")
        
        return {'search_results': videos}


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