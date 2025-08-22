from .utils import extract_youtube_page_scripts, grab_dict_by_key
from typing import Any


class YouTubeChannelsMixin:
    """Mixin class providing YouTube channel functionality"""
    
    def get_channel_videos(self, channel_id: str):
        """
        Get raw video data from a YouTube channel's videos page
        
        Args:
            channel_id (str): YouTube channel ID or handle (e.g., '@ASTRIX_official' or 'UCxxxxx')
            
        Returns:
            ChannelVideosData: Raw richGridRenderer data containing channel videos
            
        Raises:
            Exception: If channel videos data cannot be found or extracted
        """
        # Construct channel videos URL
        # Handle both @handle and channel ID formats
        if channel_id.startswith('@'):
            url = f"https://www.youtube.com/{channel_id}/videos"
        else:
            url = f"https://www.youtube.com/channel/{channel_id}/videos"
        
        # Extract scripts from the channel videos page
        scripts = extract_youtube_page_scripts(url)
        
        # Find richGridRenderer data in the scripts
        rich_grid_renderer = grab_dict_by_key(scripts, "richGridRenderer")
        
        if not rich_grid_renderer:
            raise Exception("Could not find richGridRenderer data for channel videos")
        
        # Extract the contents from richGridRenderer
        contents = rich_grid_renderer.get("richGridRenderer", {}).get("contents")
        
        if not contents:
            raise Exception("Could not find contents in richGridRenderer")
        
        return rich_grid_renderer
