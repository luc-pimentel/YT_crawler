import requests
from .utils import *
from .config import HEADERS
from .utils import extract_json_from_scripts


class SearchMixin:
    """Mixin class providing YouTube search functionality"""

    def get_search_url(self, search_term, sort_by='relevance'):
        """
        Get a filtered YouTube search URL with specified sorting.
        
        Args:
            search_term (str): The search query (e.g., "python is good")
            sort_by (str): Sorting option - one of 'relevance', 'upload_date', 'view_count', 'rating'
        
        Returns:
            str: Complete YouTube search URL with sorting applied
        
        Raises:
            ValueError: If sort_by is not a valid sorting option
            Exception: If unable to extract filter data from YouTube
        """
        
        # Define sorting options mapping
        sorting_dict = {'relevance': 0, 'upload_date': 1, 'view_count': 2, 'rating': 3}
        
        # Validate sort_by parameter
        if sort_by not in sorting_dict:
            raise ValueError(f"Invalid sort_by option. Must be one of: {list(sorting_dict.keys())}")
        
        # Format search term for URL (replace spaces with +)
        formatted_search_term = search_term.replace(' ', '+')
        
        # Base YouTube search URL
        base_url = "https://www.youtube.com"
        search_url = f"{base_url}/results?search_query={formatted_search_term}"
        
        # If relevance (default), return the base search URL
        if sort_by == 'relevance':
            return search_url
        
        try:
            # Make request to get the search page
            response = requests.get(search_url)
            response.raise_for_status()
            
            # Parse HTML
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script')
            
            # Extract JSON data containing filter information
            json_data = extract_json_from_scripts(scripts, 'searchFilterButton')
            
            if not json_data or 'searchFilterButton' not in json_data:
                raise Exception("Could not find search filter data in YouTube response")
            
            # Navigate through the nested JSON structure to get filter groups
            search_filter_groups = (json_data
                                   .get('searchFilterButton')
                                   .get('buttonRenderer')
                                   .get('command')
                                   .get('openPopupAction')
                                   .get('popup')
                                   .get('searchFilterOptionsDialogRenderer')
                                   .get('groups'))
            
            # Get the sorting filters (last group in the list)
            sorting_filters = [search_filter_group.get('searchFilterGroupRenderer').get('filters') 
                              for search_filter_group in search_filter_groups][-1]
            
            # Get the filter index for the requested sorting option
            filter_index = sorting_dict[sort_by]
            
            # Extract the URL path for the specified sorting option
            filter_url_path = (sorting_filters[filter_index]
                              .get('searchFilterRenderer')
                              .get('navigationEndpoint')
                              .get('commandMetadata')
                              .get('webCommandMetadata')
                              .get('url'))
            
            # Return complete URL
            return base_url + filter_url_path
            
        except Exception as e:
            raise Exception(f"Failed to get filtered search URL: {str(e)}")
    
    
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