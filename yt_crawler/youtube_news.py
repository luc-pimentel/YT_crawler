from .utils import *


categories_dict = {'top_stories': 0,
            'sports': 1,
            'entertainment': 2,
            'business': 3,
            'technology': 4,
            'world': 5,
            'national': 6,
            'science': 7,
            'health': 8}


class NewsMixin:
    
    def get_trending_news(self, category: str = 'top_stories') -> dict[str, Any]:
        """
        Scrapes YouTube's trending news page and returns trending video data.
        
        Args:
            category (str): The news category to fetch. Defaults to 'top_stories'.
                          Valid categories: top_stories, sports, entertainment, business,
                          technology, world, national, science, health
        
        Returns:
            dict: A dictionary containing trending news sections
            
        Raises:
            ValueError: If an invalid category is provided
        """
        # Validate category
        if category not in categories_dict:
            raise ValueError(f"Invalid category: {category}. Valid categories are: {list(categories_dict.keys())}")
        
        url = f"https://www.youtube.com/feed/news_destination/{category}"
        scripts = extract_youtube_page_scripts(url, headers=HEADERS)
        
        try:
            tabs_dict = grab_dict_by_key(scripts, 'tabs')
            if not tabs_dict:
                raise Exception('Tabs not found')
            
            tabs: list[dict[str, Any]] = tabs_dict.get('tabs', [])
            tab_contents_dict = find_nested_key(tabs[categories_dict[category]], 'contents')
            if not tab_contents_dict:
                raise Exception('Tab contents not found')

            tab_contents: list[dict[str, Any]] = tab_contents_dict.get('contents', [])
            trending_sections = [tab_content.get('richSectionRenderer', {}).get('content', {}).get('richShelfRenderer', {}) for tab_content in tab_contents]
        except (AttributeError, IndexError, TypeError):
            raise Exception("Could not parse trending news structure")
        
        return {'trending_news': trending_sections}