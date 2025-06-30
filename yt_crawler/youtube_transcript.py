import requests
from .utils import xml_transcript_to_json_bs4, extract_youtube_page_scripts, grab_dict_by_key
from .config import HEADERS
from typing import Any

class TranscriptMixin:
    
    def get_video_transcript(self, video_id: str) -> dict[str, Any]:
        """
        Get video transcript from YouTube video ID
        
        Args:
            video_id (str): YouTube video ID
            
        Returns:
            dict: Video transcript
        """
        # Construct YouTube URL
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Get the webpage content
        scripts = extract_youtube_page_scripts(youtube_url, headers=HEADERS)
        caption_tracks_dict = grab_dict_by_key(scripts, 'captionTracks')

        if not caption_tracks_dict:
            raise Exception("Could not find caption tracks")
        else:
            caption_tracks: list[dict[str, Any]] = caption_tracks_dict.get('captionTracks', [])

        base_url = next((item['baseUrl'] for item in caption_tracks if item.get('languageCode') == 'en'), None)
        if not base_url:
            raise Exception("Could not find base URL")
        
        caption_request = requests.get(base_url, headers=HEADERS)
        video_transcript = xml_transcript_to_json_bs4(caption_request.text)
        
        return video_transcript