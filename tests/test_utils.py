import sys
import os
import requests
import pytest
import warnings
from typing import Any

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from yt_crawler.utils import extract_youtube_initial_data, xml_transcript_to_json_bs4, extract_youtube_page_scripts, grab_dict_by_key
from yt_crawler.config import HEADERS


class TestExtractYoutubeInitialData:
    """Test suite for extract_youtube_initial_data function"""
    
    def test_extract_youtube_initial_data_ytInitialPlayerResponse_with_headers(self):
        """Test extracting ytInitialPlayerResponse with headers"""
        video_id = "nUgGY18iTJw"
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Test that deprecation warning is raised
        with pytest.warns(DeprecationWarning):
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
        
        # Test that deprecation warning is raised
        with pytest.warns(DeprecationWarning):
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
        
        # Test that deprecation warning is raised
        with pytest.warns(DeprecationWarning):
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
        
        # Test that deprecation warning is raised
        with pytest.warns(DeprecationWarning):
            # Call the function without headers (default None)
            result = extract_youtube_initial_data(url, 'ytInitialData')
        
        # Verify the result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Verify the dictionary is not empty
        assert len(result) > 0, "Result should not be empty"
        assert result, "Result should be truthy (not empty)"


class TestExtractYoutubePageScripts:
    """Test suite for extract_youtube_page_scripts function"""
    
    def test_extract_youtube_page_scripts_with_headers(self):
        """Test extracting YouTube page scripts with headers"""
        video_id = "nUgGY18iTJw"
        
        # Call the function with headers
        result = extract_youtube_page_scripts(video_id, headers=HEADERS)
        
        # Verify the result is a list
        assert isinstance(result, list), "Result should be a list"
        
        # Verify the list is not empty
        assert len(result) > 0, "Result should not be empty"
        
        # Verify all elements are BeautifulSoup script tags
        from bs4 import BeautifulSoup
        for script in result:
            assert hasattr(script, 'name'), "Each element should be a BeautifulSoup tag"
            assert script.name == 'script', "Each element should be a script tag"
    
    def test_extract_youtube_page_scripts_without_headers(self):
        """Test extracting YouTube page scripts without headers"""
        video_id = "nUgGY18iTJw"
        
        # Call the function without headers (default None)
        result = extract_youtube_page_scripts(video_id)
        
        # Verify the result is a list
        assert isinstance(result, list), "Result should be a list"
        
        # Verify the list is not empty
        assert len(result) > 0, "Result should not be empty"
        
        # Verify all elements are BeautifulSoup script tags
        from bs4 import BeautifulSoup
        for script in result:
            assert hasattr(script, 'name'), "Each element should be a BeautifulSoup tag"
            assert script.name == 'script', "Each element should be a script tag"


class TestGrabDictByKey:
    """Test suite for grab_dict_by_key function"""
    
    def test_grab_dict_by_key_with_headers(self):
        """Test grabbing dictionary by key with headers"""
        video_id = "nUgGY18iTJw"
        
        # First get the scripts using extract_youtube_page_scripts
        scripts = extract_youtube_page_scripts(video_id, headers=HEADERS)
        
        # Then use grab_dict_by_key to find videoDetails
        result = grab_dict_by_key(scripts, 'videoDetails')
        
        # Verify the result
        assert result is not None, "Should find videoDetails in YouTube video page"
        assert isinstance(result, dict), "Result should be a dictionary"
        assert 'videoDetails' in result, "Result should contain the target key 'videoDetails'"
        
        # Verify the structure of videoDetails
        video_details = result['videoDetails']
        assert isinstance(video_details, dict), "videoDetails should be a dictionary"
    
    def test_grab_dict_by_key_without_headers(self):
        """Test grabbing dictionary by key without headers"""
        video_id = "nUgGY18iTJw"
        
        # First get the scripts using extract_youtube_page_scripts
        scripts = extract_youtube_page_scripts(video_id)
        
        # Then use grab_dict_by_key to find videoDetails
        result = grab_dict_by_key(scripts, 'videoDetails')
        
        # Verify the result
        assert result is not None, "Should find videoDetails in YouTube video page"
        assert isinstance(result, dict), "Result should be a dictionary"
        assert 'videoDetails' in result, "Result should contain the target key 'videoDetails'"
        
        # Verify the structure of videoDetails
        video_details = result['videoDetails']
        assert isinstance(video_details, dict), "videoDetails should be a dictionary"
    
    def test_grab_dict_by_key_key_not_found(self):
        """Test grabbing dictionary by key when target key doesn't exist"""
        video_id = "nUgGY18iTJw"
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # First get the scripts using extract_youtube_page_scripts
        scripts = extract_youtube_page_scripts(url, headers=HEADERS)
        
        # Test searching for a key that doesn't exist
        result = grab_dict_by_key(scripts, 'nonExistentKey12345')
        
        # Verify the result
        assert result is None, "Should return None when target key is not found"


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
        result: dict[str, list[dict[str, Any]]] = xml_transcript_to_json_bs4(xml_content)
        
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


class TestExtractJsonFromScripts:
    """Test suite for extract_json_from_scripts function"""
    
    def test_extract_json_from_scripts_happy_path(self):
        """Test extracting JSON from scripts and finding target key - happy path"""
        from bs4 import BeautifulSoup
        from yt_crawler.utils import extract_json_from_scripts
        
        # Use a real YouTube search results page to get actual scripts
        url = "https://www.youtube.com/results?search_query=python+is+good"
        
        # Fetch the page content
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        
        # Parse with BeautifulSoup to get scripts
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script')
        
        # Test searching for searchFilterButton (known to exist in search results)
        result = extract_json_from_scripts(scripts, 'searchFilterButton')
        print(result)
        
        # Verify the result
        assert result is not None, "Should find searchFilterButton in YouTube search page"
        assert isinstance(result, dict), "Result should be a dictionary"
        assert 'searchFilterButton' in result, "Result should contain the target key"
        
        # Verify the structure of searchFilterButton
        search_filter_button = result['searchFilterButton']
        assert isinstance(search_filter_button, dict), "searchFilterButton should be a dictionary"
        assert 'buttonRenderer' in search_filter_button, "searchFilterButton should have buttonRenderer"
    
    def test_extract_json_from_scripts_key_not_found(self):
        """Test extracting JSON from scripts when target key doesn't exist"""
        from bs4 import BeautifulSoup
        from yt_crawler.utils import extract_json_from_scripts
        
        # Use a real YouTube search results page
        url = "https://www.youtube.com/results?search_query=python+is+good"
        
        # Fetch the page content
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        
        # Parse with BeautifulSoup to get scripts
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script')
        
        # Test searching for a key that doesn't exist
        result = extract_json_from_scripts(scripts, 'nonExistentKey12345')
        
        # Verify the result
        assert result is None, "Should return None when target key is not found"