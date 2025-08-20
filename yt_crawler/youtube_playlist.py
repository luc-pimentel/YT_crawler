from .utils import *


class PlaylistMixin:
    """Mixin class for YouTube playlist functionality"""
    
    def get_playlist_videos(self, playlist_id: str) -> dict[str, Any]:
        """
        Get playlist videos from YouTube playlist ID
        
        Args:
            playlist_id (str): YouTube playlist ID
            
        Returns:
            dict: Playlist videos data wrapped in 'playlist_videos' key
        """
        # Get the webpage content
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        scripts = extract_youtube_page_scripts(url, headers=HEADERS)
        
        playlist_data_dict = grab_dict_by_key(scripts, 'playlistVideoListRenderer')
        if not playlist_data_dict:
            raise Exception("No playlist data found")
        
        playlist_video_list_renderer = playlist_data_dict.get('playlistVideoListRenderer')
        if not playlist_video_list_renderer:
            raise Exception("No playlistVideoListRenderer found")
            
        playlist_contents = playlist_video_list_renderer.get('contents')
        if not playlist_contents:
            raise Exception("No playlist contents found")

        # Wrap in playlist_videos dictionary
        playlist_videos = {
            'playlist_videos': playlist_contents
        }
        
        return playlist_videos


    def get_playlist_details(self, playlist_id: str) -> dict[str, Any]:
        """
        Get playlist details from YouTube playlist ID
        
        Args:
            playlist_id (str): YouTube playlist ID
            
        Returns:
            dict: Playlist details with first 2 keys wrapped in 'playlist_details' key
        """
        # Get the webpage content
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        scripts = extract_youtube_page_scripts(url, headers=HEADERS)
        
        playlist_data_dict = grab_dict_by_key(scripts, 'pageHeaderViewModel').get('pageHeaderViewModel')
        
        # Keep only the title and metadata keys from the playlist data
        if playlist_data_dict:
            keys_to_keep = ['title', 'metadata']
            filtered_data = {key: playlist_data_dict[key] for key in keys_to_keep if key in playlist_data_dict}
        else:
            filtered_data = {}
        
        # Wrap in playlist_details dictionary
        return {'playlist_details': filtered_data}

