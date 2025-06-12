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
    
    def get_trending_news(self, category='top_stories'):
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
        initial_data_response_json = extract_youtube_initial_data(url, 'ytInitialData')
        #return initial_data_response_json
        
        try:
            tabs = initial_data_response_json.get('contents').get('twoColumnBrowseResultsRenderer').get('tabs')
            tab_contents = tabs[categories_dict[category]].get('tabRenderer').get('content').get('richGridRenderer').get('contents')
            trending_sections = [tab_content.get('richSectionRenderer').get('content').get('richShelfRenderer') for tab_content in tab_contents]
        except (AttributeError, IndexError, TypeError):
            raise Exception("Could not parse trending news structure")
        
        return {'trending_news': trending_sections}