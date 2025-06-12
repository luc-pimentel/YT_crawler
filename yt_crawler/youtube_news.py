from .utils import *


class NewsMixin:
    
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