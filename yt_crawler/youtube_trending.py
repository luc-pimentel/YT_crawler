from .utils import *


class TrendingMixin:
    
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