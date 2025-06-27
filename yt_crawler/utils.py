from bs4 import BeautifulSoup
import requests
import json
import re
from .config import HEADERS
from typing import Any

def xml_transcript_to_json_bs4(xml_string: str) -> dict[str, Any]:
    """Convert YouTube transcript XML to JSON using BeautifulSoup"""
    soup = BeautifulSoup(xml_string, 'xml')
    
    transcript_data: dict[str, Any] = {
        "transcript": []
    }
    
    # Find all text elements
    text_elements = soup.find_all('text')
    
    for text_elem in text_elements:
        entry = {
            "start": float(text_elem.get('start')),
            "duration": float(text_elem.get('dur')),
            "text": text_elem.get_text() or ""
        }
        transcript_data["transcript"].append(entry)

    return transcript_data


def extract_youtube_initial_data(url: str, variable_name: str = 'ytInitialData', headers: dict[str, str] | None = None, payload: dict[str, Any] | None = None) -> dict[str, Any] | None:
    """
    Extract YouTube initial data from a given URL.
    
    Args:
        url (str): YouTube URL to scrape
        variable_name (str): JavaScript variable name to extract ('ytInitialData' or 'ytInitialPlayerResponse')
        headers (dict, optional): Custom headers for the request
        
    Returns:
        dict: Parsed JSON data from the JavaScript variable
        
    Raises:
        Exception: If the variable is not found or JSON parsing fails
    """
    
    # Get the webpage content
    response = requests.get(url, headers=headers, json=payload)
    response.raise_for_status()
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all script tags
    scripts = soup.find_all('script')
    # Find the script text containing the target variable
    script_text = next(
        (script.text.split(f'var {variable_name} = ')[1][:-1]
         for script in scripts 
         if script.string and f'var {variable_name} = ' in script.string),
        None
    )
    
    if not script_text:
        raise Exception(f"Could not find {variable_name} in page source")
    
    try:
        # Parse the JSON from the script text
        return json.loads(script_text)
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse {variable_name} JSON: {str(e)}")
    

def find_nested_key(obj: dict[str, Any] | list[Any] | Any, target_key: str) -> dict[str, Any] | None:
    """
    Recursively search for a key in nested dictionaries/lists
    
    Args:
        obj: The object to search in (dict, list, or other)
        target_key (str): The key to search for
        
    Returns:
        dict: The dictionary containing the target key, or None if not found
    """
    if isinstance(obj, dict):
        if target_key in obj:
            return obj
        for value in obj.values():
            result = find_nested_key(value, target_key)
            if result is not None:
                return result
    elif isinstance(obj, list):
        for item in obj:
            result = find_nested_key(item, target_key)
            if result is not None:
                return result
    return None


def extract_json_from_scripts(scripts: list[BeautifulSoup], target_key: str) -> dict[str, Any] | None:
    """
    Extract and parse JSON data from BeautifulSoup script elements, searching for a specific key
    
    Args:
        scripts: List of BeautifulSoup script elements
        target_key (str): The key to search for in the parsed JSON data
        
    Returns:
        dict: The dictionary containing the target key, or None if not found
    """
    for script in scripts:
        if script.string:  # Check if script has content
            try:
                # Extract potential JSON from script content
                script_content = script.string.strip()
                
                # Look for JSON-like patterns
                json_matches = re.findall(r'\{.*\}', script_content, re.DOTALL)
                
                for json_str in json_matches:
                    try:
                        data = json.loads(json_str)
                        result = find_nested_key(data, target_key)
                        if result:
                            return result
                    except json.JSONDecodeError:
                        continue
                        
            except Exception:
                continue
    
    return None


def fetch_youtube_continuation_data(continuation_token: str, click_tracking_params: str, api_url: str) -> dict[str, Any]:
    """
    Fetch YouTube comments data using continuation token and click tracking params.
    
    Args:
        continuation_token (str): The continuation token for pagination
        click_tracking_params (str): The click tracking parameters
        
    Returns:
        dict: Parsed JSON response from YouTube API
        
    Raises:
        Exception: If the API request fails
    """
    comment_url = f"https://www.youtube.com{api_url}"
    
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
        return response.json()
    else:
        raise Exception(f"Failed to fetch comments: HTTP {response.status_code}")