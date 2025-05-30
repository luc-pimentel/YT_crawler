from bs4 import BeautifulSoup

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