import requests
from bs4 import BeautifulSoup
import json
from .utils import *
from .config import HEADERS
from .youtube_search import SearchMixin

class YoutubeAPI(SearchMixin):

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
    

    def get_video_comments(self, video_id, n_comments=None):
        """
        Get video comments from YouTube video ID
            
        Args:
            video_id (str): YouTube video ID
            n_comments (int, optional): Maximum number of comments to fetch. If None, fetches all comments.
                
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


        all_comments = []
        
        while continuation_token:
            data = fetch_youtube_continuation_data(continuation_token, click_tracking_params, '/youtubei/v1/next?prettyPrint=false')
            
            try:
                mutations_list = data.get('frameworkUpdates').get('entityBatchUpdate').get('mutations')
                comments = [mutation.get('payload').get('commentEntityPayload') for mutation in mutations_list if 'commentEntityPayload' in mutation.get('payload').keys()]
                all_comments.extend(comments)
            except (AttributeError, TypeError):
                raise Exception("Could not parse comment data from response")
            
            # Check if we've reached the desired number of comments
            if n_comments is not None and len(all_comments) >= n_comments:
                break
            
            # Extract continuation data for next batch - handle both possible response structures
            try:
                response_endpoint = data.get('onResponseReceivedEndpoints')[-1]
                
                # Try 'reloadContinuationItemsCommand' first
                if 'reloadContinuationItemsCommand' in response_endpoint:
                    continuation_item_renderer = response_endpoint.get('reloadContinuationItemsCommand').get('continuationItems')[-1]
                # Fall back to 'appendContinuationItemsAction'
                elif 'appendContinuationItemsAction' in response_endpoint:
                    continuation_item_renderer = response_endpoint.get('appendContinuationItemsAction').get('continuationItems')[-1]
                else:
                    # Neither key found, no more continuation data
                    continuation_token = None
                    continue
                
                continuation_token = continuation_item_renderer.get('continuationItemRenderer').get('continuationEndpoint').get('continuationCommand').get('token')
                click_tracking_params = continuation_item_renderer.get('continuationItemRenderer').get('continuationEndpoint').get('clickTrackingParams')
            except (AttributeError, IndexError, TypeError):
                # No more continuation data available
                continuation_token = None

        # Truncate to exact number if n_comments is specified
        if n_comments is not None:
            all_comments = all_comments[:n_comments]

        comments_json = {'comments': all_comments}
        return comments_json
    

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