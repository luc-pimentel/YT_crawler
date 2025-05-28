import youtubesearchpython as yts
from .exceptions import NoAPIKeyException
from decouple import config
from typing import Union
import os
import warnings



YOUTUBE_API_KEY = config('YOUTUBE_API_KEY', None)


class YoutubeAPI:
    base_url: str = 'https://www.googleapis.com/youtube/v3/'
    api_error_message: str = "An API key is necessary for this method. Please visit the YouTube Data API v3 to obtain one: https://developers.google.com/youtube/v3/"

    def __init__(self, api_key: str = YOUTUBE_API_KEY):

#        api_key = self._get_api_key(api_key, "YOUTUBE_API_KEY",
#                                    action='warn',
#                                    message="""No Youtube V3 API key provided. Some methods may not work.
#                                    Please set the YOUTUBE_API_KEY environment variable using os.environ['YOUTUBE_API_KEY'] or pass it to the object via the api_key parameter."""
#                                    )
        
        self.api_key = api_key
        super().__init__()
        
    
    def _check_api_key(self):
        if self.api_key is None:
            raise NoAPIKeyException(self.api_error_message)


    def get(self, endpoint, params=None, **kwargs):
        if params is None:
            params = {}
        params['key'] = self.api_key
        return super().get(endpoint, params=params, **kwargs)


    def search(self, query:str, results:int = 10, **kwargs):
        '''Search youtube videos'''
        return yts.VideosSearch(query, limit = results, **kwargs).result()
    
    def get_full_video_info(self, video_id):
        video_info = yts.Video.getInfo(video_id)
        return video_info
        

    def search_channel(self, query, limit=10, region=None, **kwargs):
        channels_search = yts.ChannelsSearch(query, limit=limit, region=region, **kwargs)
        return channels_search.result()
