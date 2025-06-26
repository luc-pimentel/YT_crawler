import requests
from .utils import *
from .config import HEADERS
from .utils import extract_json_from_scripts


SEARCH_FILTER_DICT = {
    'upload_date': {
        'index': 0,
        'options': {
            'last_hour': 0,
            'today': 1, 
            'this_week': 2,
            'this_month': 3,
            'this_year': 4
        }
    },
    'type': {
        'index': 1,
        'options': {
            'video': 0,
            'channel': 1,
            'playlist': 2,
            'movie': 3
        }
    },
    'duration': {
        'index': 2,
        'options': {
            'under_4_minutes': 0,
            '4_20_minutes': 1,
            'over_20_minutes': 2
        }
    },
    'features': {
        'index': 3,
        'options': {
            'live': 0,
            '4k': 1,
            'hd': 2,
            'subtitles_cc': 3,
            'creative_commons': 4,
            '360': 5,
            'vr180': 6,
            '3d': 7,
            'hdr': 8,
            'location': 9,
            'purchased': 10
        }
    },
    'sort_by': {
        'index': 4,
        'options': {
            'relevance': 0,
            'upload_date': 1,
            'view_count': 2,
            'rating': 3
        }
    }
}



class SearchMixin:
    """Mixin class providing YouTube search functionality"""


    def _get_search_url(self, search_term: str, upload_date: str | None = None, duration: str | None = None, features: str | None = None, sort_by: str = 'relevance') -> str:
        """
        Get a filtered YouTube search URL with specified filters.
        
        Args:
            search_term (str): The search query (e.g., "python is good")
            upload_date (str): Upload date filter - one of 'last_hour', 'today', 'this_week', 'this_month', 'this_year'
            type (str): Content type filter - one of 'video', 'channel', 'playlist', 'movie'
            duration (str): Duration filter - one of 'under_4_minutes', '4_20_minutes', 'over_20_minutes'
            features (str): Features filter - one of 'live', '4k', 'hd', 'subtitles_cc', 'creative_commons', '360', 'vr180', '3d', 'hdr', 'location', 'purchased'
            sort_by (str): Sorting option - one of 'relevance', 'upload_date', 'view_count', 'rating'
        
        Returns:
            str: Complete YouTube search URL with filters applied
        
        Raises:
            ValueError: If any filter option is not valid
            Exception: If unable to extract filter data from YouTube
        """
        type=None # Type filter is not supported yet
        
        # Format search term for URL (replace spaces with +)
        formatted_search_term = search_term.replace(' ', '+')
        
        # Base YouTube search URL
        base_url = "https://www.youtube.com"
        current_url = f"{base_url}/results?search_query={formatted_search_term}"
        
        # Collect active filters
        active_filters = {}
        filter_params = {
            'upload_date': upload_date,
            'type': type,
            'duration': duration,
            'features': features,
            'sort_by': sort_by
        }
        
        # Validate and collect non-None filters (except sort_by='relevance' which is default)
        for filter_name, filter_value in filter_params.items():
            if filter_value is not None:
                if filter_name == 'sort_by' and filter_value == 'relevance':
                    continue  # Skip default sort_by
                
                if filter_name not in SEARCH_FILTER_DICT:
                    raise ValueError(f"Unknown filter type: {filter_name}")
                
                filter_options = SEARCH_FILTER_DICT[filter_name]['options']
                if filter_value not in filter_options:
                    raise ValueError(f"Invalid {filter_name} option '{filter_value}'. Must be one of: {list(filter_options.keys())}")
                
                active_filters[filter_name] = filter_value
        
        # If no filters are active, return base search URL
        if not active_filters:
            return current_url
        
        # Apply filters sequentially
        for filter_name, filter_value in active_filters.items():
            try:
                
                # Make request to get the current page
                response = requests.get(current_url)
                response.raise_for_status()
                
                # Parse HTML
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                scripts = soup.find_all('script')
                
                # Extract JSON data containing filter information
                json_data = extract_json_from_scripts(scripts, 'searchFilterButton')
                
                if not json_data or 'searchFilterButton' not in json_data:
                    raise Exception(f"Could not find search filter data when applying {filter_name} filter")
                
                # Navigate through the nested JSON structure to get filter groups
                search_filter_groups = (json_data
                                    .get('searchFilterButton', {})
                                    .get('buttonRenderer', {})
                                    .get('command', {})
                                    .get('openPopupAction', {})
                                    .get('popup', {})
                                    .get('searchFilterOptionsDialogRenderer', {})
                                    .get('groups', []))
                
                # Get the filter group index and option index
                filter_group_index = SEARCH_FILTER_DICT[filter_name]['index']
                option_index = SEARCH_FILTER_DICT[filter_name]['options'][filter_value]
                
                # Get the specific filter group
                filter_group = search_filter_groups[filter_group_index]
                filters = filter_group.get('searchFilterGroupRenderer').get('filters')
                
                # Extract the URL path for the specified filter option
                filter_url_path = (filters[option_index]
                                .get('searchFilterRenderer')
                                .get('navigationEndpoint')
                                .get('commandMetadata')
                                .get('webCommandMetadata')
                                .get('url'))
                
                # Update current URL for next iteration
                current_url = base_url + filter_url_path
                
            except Exception as e:
                raise Exception(f"Failed to apply {filter_name} filter with value '{filter_value}': {str(e)}")
        
        return current_url
    

    def search(self, search_term: str, n_videos: int = 100, upload_date: str | None = None, duration: str | None = None, features: str | None = None, sort_by: str = 'relevance') -> dict:
        """
        Search YouTube videos
        
        Args:
            search_term (str): Search query
            n_videos (int): Number of videos to retrieve
            upload_date (str): Upload date filter - one of 'last_hour', 'today', 'this_week', 'this_month', 'this_year'
            duration (str): Duration filter - one of 'under_4_minutes', '4_20_minutes', 'over_20_minutes'
            features (str): Features filter - one of 'live', '4k', 'hd', 'subtitles_cc', 'creative_commons', '360', 'vr180', '3d', 'hdr', 'location', 'purchased'
            sort_by (str): Sorting option - one of 'relevance', 'upload_date', 'view_count', 'rating'
            
        Returns:
            dict: Search results
        """
        
        # Use the updated _get_search_url method to construct the URL with all filters
        url = self._get_search_url(search_term, upload_date, duration, features, sort_by)
        raw_search_json = extract_youtube_initial_data(url, 'ytInitialData')
        if not raw_search_json:
            raise Exception("Could not find initial data response JSON")
        
        try:
            search_contents = raw_search_json.get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [])
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
                
                continuation_items = continuation_data.get('onResponseReceivedCommands', [])[0].get('appendContinuationItemsAction', {}).get('continuationItems', [])
                
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