from bs4 import BeautifulSoup
import requests
import json
from .config import HEADERS

def xml_transcript_to_json_bs4(xml_string):
    """Convert YouTube transcript XML to JSON using BeautifulSoup"""
    soup = BeautifulSoup(xml_string, 'xml')
    
    transcript_data = {
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


def extract_youtube_initial_data(url, variable_name='ytInitialData', headers=None):
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
    response = requests.get(url, headers=headers)
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