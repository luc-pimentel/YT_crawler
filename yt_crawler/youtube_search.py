import requests
from .utils import *
from .config import HEADERS


class SearchMixin:
    """Mixin class providing YouTube search functionality"""
    
    def search(self, search_term: str, n_videos: int = 50):
        """
        Search YouTube videos
        
        Args:
            search_term (str): Search query
            n_videos (int): Number of videos to retrieve
            
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
        
        try:
            click_tracking_params = search_contents[1].get('continuationItemRenderer').get('continuationEndpoint').get('clickTrackingParams')
            continuation_token = search_contents[1].get('continuationItemRenderer').get('continuationEndpoint').get('continuationCommand').get('token')
        except (AttributeError, IndexError, TypeError):
            raise Exception("Could not parse search results")
        
        # Fetch additional batches until we have enough videos
        all_videos = videos
        while len(all_videos) < n_videos and continuation_token:
            try:
                continuation_data = fetch_youtube_continuation_data(continuation_token, click_tracking_params, '/youtubei/v1/search')
                
                continuation_items = continuation_data.get('onResponseReceivedCommands')[0].get('appendContinuationItemsAction').get('continuationItems')
                
                next_set_of_videos = continuation_items[0].get('itemSectionRenderer').get('contents')
                next_videos = [video.get('videoRenderer') for video in next_set_of_videos if video.get('videoRenderer')]
                
                all_videos.extend(next_videos)
                
                # Update continuation token for next iteration
                continuation_token = continuation_items[1].get('continuationItemRenderer').get('continuationEndpoint').get('continuationCommand').get('token')
                click_tracking_params = continuation_items[1].get('continuationItemRenderer').get('continuationEndpoint').get('clickTrackingParams')
                
            except (AttributeError, IndexError, TypeError, KeyError):
                # No more continuation data available
                break
        
        return {'search_results': all_videos[:n_videos]}