import requests
from bs4 import BeautifulSoup
import json
from decouple import config
from .utils import xml_transcript_to_json_bs4


YOUTUBE_API_KEY = config('YOUTUBE_API_KEY', None)


class YoutubeAPI:


    def get_video_details(self, video_id):
        """
        Get video details from YouTube video ID
        
        Args:
            video_id (str): YouTube video ID
            
        Returns:
            dict: Video details including title, description, view count etc.
        """
        # Construct YouTube URL
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Get the webpage content
        r = requests.get(youtube_url)
        r.raise_for_status()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Find all script tags
        scripts = soup.find_all('script')
        
        # Find the script text containing ytInitialPlayerResponse
        script_text = next(
            (script.text.split('var ytInitialPlayerResponse = ')[1][:-1]
            for script in scripts 
            if script.string and 'var ytInitialPlayerResponse = ' in script.string),
            None
        )
        
        # Parse the JSON from the script text
        initial_player_response_json = json.loads(script_text) if script_text else {}

        video_details = initial_player_response_json.get('videoDetails')

        if not video_details:
            raise Exception("No video details found")
        
        return video_details
    

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
        r = requests.get(youtube_url)
        r.raise_for_status()
            
            # Parse with BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
            
            # Find all script tags
        scripts = soup.find_all('script')
            
            # Find the script text containing ytInitialPlayerResponse
        script_text = next(
                (script.text.split('var ytInitialPlayerResponse = ')[1][:-1]
                for script in scripts 
                if script.string and 'var ytInitialPlayerResponse = ' in script.string),
                None
            )
            
            # Parse the JSON from the script text
        initial_player_response_json = json.loads(script_text) if script_text else {}

        caption_url = initial_player_response_json.get('captions').get('playerCaptionsTracklistRenderer').get('captionTracks')[0].get('baseUrl')
        caption_request = requests.get(caption_url)
        video_transcript = xml_transcript_to_json_bs4(caption_request.text)

        return video_transcript
