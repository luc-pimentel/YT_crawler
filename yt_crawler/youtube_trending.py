from .utils import *


trending_category_dict = {'now': 0,
                         'music': 1,
                         'gaming': 2,
                         'movies': 3}


class TrendingMixin:
    
    def get_trending_videos(self, category: str = 'now') -> dict[str, Any]:
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
            scripts = extract_youtube_page_scripts(url, headers=HEADERS)
        else:
            # For other categories, first get the main trending page to extract category URL
            main_url = base_url + "/feed/trending"
            scripts = extract_youtube_page_scripts(main_url, headers=HEADERS)
            
            
            try:
                tabs_dict = grab_dict_by_key(scripts, 'tabs')
                if not tabs_dict:
                    raise Exception('Trending tabs not found')
                
                tabs:list[dict[str, Any]] = tabs_dict.get('tabs', [])
                category_url: str = tabs[category_index].get('tabRenderer', {}).get('endpoint', {}).get('commandMetadata', {}).get('webCommandMetadata', {}).get('url', '')
                
                # Make request to category-specific URL
                url = base_url + category_url
                scripts = extract_youtube_page_scripts(url, headers=HEADERS)
            except (AttributeError, IndexError, TypeError):
                raise Exception(f"Could not extract URL for category '{category}'")
        
        try:
            tabs_dict = grab_dict_by_key(scripts, 'tabs')
            if not tabs_dict:
                raise Exception('Trending tabs not found')
            else:
                tabs:list[dict[str, Any]] = tabs_dict.get('tabs', [])

            contents_dict = find_nested_key(tabs[category_index], 'contents')
            if not contents_dict:
                raise Exception('Contents not found')
            else:
                contents: list = contents_dict.get('contents', [])
        except (AttributeError, IndexError, TypeError):
            raise Exception(f"Could not parse trending videos structure for category '{category}'")
        
        videos_list: list[dict[str, Any]] = []
        
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