from .utils import *


trending_category_dict = {'now': 0,
                         'music': 1,
                         'gaming': 2,
                         'movies': 3}


class TrendingMixin:
    
    def get_trending_videos(self, category: str = 'now') -> dict:
        """
        Scrapes YouTube trending videos and returns them in a structured format.
        
        Args:
            category (str): Trending category to fetch. Options: 'now', 'music', 'gaming', 'movies'
        
        Returns:
            dict: Dictionary containing trending videos list
        """
        # Validate category
        if category not in trending_category_dict:
            raise ValueError(f"Invalid category '{category}'. Valid options: {list(trending_category_dict.keys())}")
        
        category_index = trending_category_dict[category]
        base_url = "https://www.youtube.com"
        
        if category == 'now':
            # Use existing logic for 'now' category
            url = base_url + "/feed/trending"
            raw_search_json = extract_youtube_initial_data(url, 'ytInitialData')
            if not raw_search_json:
                raise Exception("Could not find initial data response JSON")
            content_tab_index = 0
        else:
            # For other categories, first get the main trending page to extract category URL
            main_url = base_url + "/feed/trending"
            main_json = extract_youtube_initial_data(main_url, 'ytInitialData')
            if not main_json:
                raise Exception("Could not find initial data response JSON")
            
            try:
                tabs = main_json.get('contents', {}).get('twoColumnBrowseResultsRenderer', {}).get('tabs', [])
                category_url = tabs[category_index].get('tabRenderer').get('endpoint').get('commandMetadata').get('webCommandMetadata').get('url')
                
                # Make request to category-specific URL
                url = base_url + category_url
                raw_search_json = extract_youtube_initial_data(url, 'ytInitialData')
                if not raw_search_json:
                    raise Exception("Could not find initial data response JSON")
                content_tab_index = category_index
            except (AttributeError, IndexError, TypeError):
                raise Exception(f"Could not extract URL for category '{category}'")
        
        try:
            tabs = raw_search_json.get('contents', {}).get('twoColumnBrowseResultsRenderer', {}).get('tabs', [])
            contents = tabs[content_tab_index].get('tabRenderer').get('content').get('sectionListRenderer').get('contents')
        except (AttributeError, IndexError, TypeError):
            raise Exception(f"Could not parse trending videos structure for category '{category}'")
        
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
                
                videos_list.extend([video.get('videoRenderer') for video in videos if 'videoRenderer' in video])
            except (AttributeError, TypeError):
                # Skip sections that don't match expected structure
                continue
        
        return {'trending': videos_list}