import pytest
import sys
import os
import requests

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from yt_crawler.utils import extract_youtube_initial_data, xml_transcript_to_json_bs4
from yt_crawler.config import HEADERS


class TestExtractYoutubeInitialData:
    """Test suite for extract_youtube_initial_data function"""
    
    def test_extract_youtube_initial_data_ytInitialPlayerResponse_with_headers(self):
        """Test extracting ytInitialPlayerResponse with headers"""
        video_id = "nUgGY18iTJw"
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Call the function with headers
        result = extract_youtube_initial_data(url, 'ytInitialPlayerResponse', HEADERS)
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary is not empty
        assert len(result) > 0, "Result should not be empty"
        assert result, "Result should be truthy (not empty)"
    
    def test_extract_youtube_initial_data_ytInitialPlayerResponse_without_headers(self):
        """Test extracting ytInitialPlayerResponse without headers"""
        video_id = "nUgGY18iTJw"
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Call the function without headers (default None)
        result = extract_youtube_initial_data(url, 'ytInitialPlayerResponse')
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary is not empty
        assert len(result) > 0, "Result should not be empty"
        assert result, "Result should be truthy (not empty)"
    
    def test_extract_youtube_initial_data_ytInitialData_with_headers(self):
        """Test extracting ytInitialData with headers"""
        url = "https://www.youtube.com/results?search_query=python"
        
        # Call the function with headers
        result = extract_youtube_initial_data(url, 'ytInitialData', HEADERS)
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary is not empty
        assert len(result) > 0, "Result should not be empty"
        assert result, "Result should be truthy (not empty)"
    
    def test_extract_youtube_initial_data_ytInitialData_without_headers(self):
        """Test extracting ytInitialData without headers"""
        url = "https://www.youtube.com/results?search_query=python"
        
        # Call the function without headers (default None)
        result = extract_youtube_initial_data(url, 'ytInitialData')
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary is not empty
        assert len(result) > 0, "Result should not be empty"
        assert result, "Result should be truthy (not empty)"



class TestXmlTranscriptToJsonBs4:
    """Test suite for xml_transcript_to_json_bs4 function"""
    
    def test_xml_transcript_to_json_bs4_with_youtube_transcript(self):
        """Test converting YouTube transcript XML to JSON"""
        transcript_url = "https://www.youtube.com/api/timedtext?v=nUgGY18iTJw&ei=JIQ_aO3rAfyNobIPubLmmA4&caps=asr&opi=112496729&xoaf=5&hl=pt&ip=0.0.0.0&ipbits=0&expire=1749018260&sparams=ip,ipbits,expire,v,ei,caps,opi,xoaf&signature=291189FCE2558A69EE7B24ED6F4C48E24FA21B2F.22D4D0FB00B6A6CAB3F89334B2768FCC1BAD021F&key=yt8&kind=asr&lang=en"
        
        # Fetch the XML transcript data
        response = requests.get(transcript_url, headers=HEADERS)
        response.raise_for_status()
        xml_content = response.text
        
        # Call the function
        result = xml_transcript_to_json_bs4(xml_content)
        
        # Verify the result structure
        assert isinstance(result, dict), "Result should be a dictionary"
        assert "transcript" in result, "Result should contain 'transcript' key"
        assert isinstance(result["transcript"], list), "Transcript should be a list"
        assert len(result["transcript"]) > 0, "Transcript should not be empty"
        
        # Verify the structure of transcript entries
        for entry in result["transcript"]:
            assert isinstance(entry, dict), "Each transcript entry should be a dictionary"
            assert "start" in entry, "Entry should have 'start' field"
            assert "duration" in entry, "Entry should have 'duration' field"
            assert "text" in entry, "Entry should have 'text' field"
            
            # Verify data types
            assert isinstance(entry["start"], float), "Start should be a float"
            assert isinstance(entry["duration"], float), "Duration should be a float"
            assert isinstance(entry["text"], str), "Text should be a string"