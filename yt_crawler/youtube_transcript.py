import requests
from .utils import extract_youtube_initial_data, xml_transcript_to_json_bs4


class TranscriptMixin:
    
    def get_video_transcript(self, video_id):
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
        initial_player_response_json = extract_youtube_initial_data(youtube_url, 'ytInitialPlayerResponse')

        captions_element = initial_player_response_json.get('captions')

        if not captions_element:
            raise Exception("Video has no transcript available")

        caption_url = captions_element.get('playerCaptionsTracklistRenderer').get('captionTracks')[0].get('baseUrl')
        caption_request = requests.get(caption_url)
        video_transcript = xml_transcript_to_json_bs4(caption_request.text)

        return video_transcript 