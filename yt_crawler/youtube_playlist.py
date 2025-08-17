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
