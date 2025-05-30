import requests
from bs4 import BeautifulSoup
import json
from .utils import xml_transcript_to_json_bs4
from .config import HEADERS



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
    

    def get_video_comments(self, video_id):
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
            (script.text.split('var ytInitialData = ')[1][:-1]
            for script in scripts 
            if script.string and 'var ytInitialData = ' in script.string),
            None
        )
            
            # Parse the JSON from the script text
        initial_data_response_json = json.loads(script_text) if script_text else {}


        comment_section_renderer_json = initial_data_response_json.get('engagementPanels')[0].get('engagementPanelSectionListRenderer').get('content').get('sectionListRenderer').get('contents')[0]

        continuation_endpoint = comment_section_renderer_json.get('itemSectionRenderer').get('contents')[0].get('continuationItemRenderer').get('continuationEndpoint')

        click_tracking_params = continuation_endpoint.get('clickTrackingParams')
        continuation_token = continuation_endpoint.get('continuationCommand').get('token')


        comment_url = "https://www.youtube.com/youtubei/v1/next?prettyPrint=false"

        # Payload with continuation and click tracking
        payload = {
            "context": {
                "client": {
                    "clientName": "WEB",
                    "clientVersion": "2.20240321.08.00",
                    "clientScreen": "WATCH"
                }
            },
            "continuation": continuation_token,
            "clickTracking": {
                "clickTrackingParams": click_tracking_params
            }
        }

        response = requests.post(comment_url, json=payload, headers=HEADERS)

        # Check the response
        if response.status_code == 200:
            data = response.json()

        mutations_list = data.get('frameworkUpdates').get('entityBatchUpdate').get('mutations')

        comments = [mutation.get('payload') for mutation in mutations_list if 'commentEntityPayload' in mutation.get('payload').keys()]

        comments_json = {'comments': comments}

        return comments_json
    

    def search(self, search_term):
        # URL encode the search term to handle spaces and special characters
        quoted_search_term = requests.utils.quote(search_term)
        url = f"https://www.youtube.com/results?search_query={quoted_search_term}"
        
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        soup_str = str(soup.find_all()[0])
        raw_search_json = json.loads(soup_str.split('var ytInitialData = ')[1].split('};')[0] + '}')
        
        search_contents = raw_search_json.get('contents').get('twoColumnSearchResultsRenderer').get('primaryContents').get('sectionListRenderer').get('contents')
        
        item_section_renderer_contents = search_contents[0].get('itemSectionRenderer').get('contents')
        
        videos = [video.get('videoRenderer') for video in item_section_renderer_contents if video.get('videoRenderer')]
        
        return {'search_results': videos}

