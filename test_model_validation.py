# Auto-generated model validation test
import json
from pydantic import ValidationError

"""
Pydantic models for YouTube video details API response.

Generated from video_details.json structure with comprehensive type mapping,
validation rules, and proper field definitions.
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import List
from datetime import datetime


class ThumbnailItem(BaseModel):
    """Individual thumbnail image with dimensions."""
    
    url: HttpUrl = Field(..., description="Direct URL to the thumbnail image")
    width: int = Field(..., description="Thumbnail width in pixels")
    height: int = Field(..., description="Thumbnail height in pixels")


class ThumbnailContainer(BaseModel):
    """Container for thumbnail images."""
    
    thumbnails: List[ThumbnailItem] = Field(..., description="List of available thumbnail sizes")


class VideoDetails(BaseModel):
    """Core video details and metadata."""
    
    video_id: str = Field(..., alias="videoId", description="Unique YouTube video identifier")
    title: str = Field(..., description="Video title")
    length_seconds: str = Field(..., alias="lengthSeconds", description="Video duration in seconds as string")
    keywords: List[str] = Field(..., description="Video keywords/tags")
    channel_id: str = Field(..., alias="channelId", description="YouTube channel identifier")
    is_owner_viewing: bool = Field(..., alias="isOwnerViewing", description="Whether the owner is viewing")
    short_description: str = Field(..., alias="shortDescription", description="Brief video description")
    is_crawlable: bool = Field(..., alias="isCrawlable", description="Whether video is crawlable by search engines")
    thumbnail: ThumbnailContainer = Field(..., description="Video thumbnail information")
    allow_ratings: bool = Field(..., alias="allowRatings", description="Whether ratings are allowed")
    view_count: str = Field(..., alias="viewCount", description="View count as string")
    author: str = Field(..., description="Channel/author name")
    is_private: bool = Field(..., alias="isPrivate", description="Whether video is private")
    is_unplugged_corpus: bool = Field(..., alias="isUnpluggedCorpus", description="Unplugged corpus status")
    is_live_content: bool = Field(..., alias="isLiveContent", description="Whether this is live content")


class EmbedInfo(BaseModel):
    """Video embed information."""
    
    iframe_url: HttpUrl = Field(..., alias="iframeUrl", description="Embed iframe URL")
    width: int = Field(..., description="Embed width in pixels")
    height: int = Field(..., description="Embed height in pixels")


class SimpleText(BaseModel):
    """Simple text container."""
    
    simple_text: str = Field(..., alias="simpleText", description="Plain text content")


class PlayerMicroformatRenderer(BaseModel):
    """Detailed microformat information for the video player."""
    
    thumbnail: ThumbnailContainer = Field(..., description="Microformat thumbnail information")
    embed: EmbedInfo = Field(..., description="Video embed configuration")
    title: SimpleText = Field(..., description="Video title in simple text format")
    description: SimpleText = Field(..., description="Video description in simple text format")
    length_seconds: str = Field(..., alias="lengthSeconds", description="Video duration in seconds")
    owner_profile_url: HttpUrl = Field(..., alias="ownerProfileUrl", description="Channel owner profile URL")
    external_channel_id: str = Field(..., alias="externalChannelId", description="External channel identifier")
    is_family_safe: bool = Field(..., alias="isFamilySafe", description="Whether content is family safe")
    available_countries: List[str] = Field(..., alias="availableCountries", description="Countries where video is available")
    is_unlisted: bool = Field(..., alias="isUnlisted", description="Whether video is unlisted")
    has_ypc_metadata: bool = Field(..., alias="hasYpcMetadata", description="Whether has YPC metadata")
    view_count: str = Field(..., alias="viewCount", description="View count as string")
    category: str = Field(..., description="Video category")
    publish_date: datetime = Field(..., alias="publishDate", description="Video publish date")
    owner_channel_name: str = Field(..., alias="ownerChannelName", description="Channel owner name")
    upload_date: datetime = Field(..., alias="uploadDate", description="Video upload date")
    is_shorts_eligible: bool = Field(..., alias="isShortsEligible", description="Whether eligible for YouTube Shorts")
    external_video_id: str = Field(..., alias="externalVideoId", description="External video identifier")
    like_count: str = Field(..., alias="likeCount", description="Like count as string")
    canonical_url: HttpUrl = Field(..., alias="canonicalUrl", description="Canonical video URL")


class Microformat(BaseModel):
    """Microformat data container."""
    
    player_microformat_renderer: PlayerMicroformatRenderer = Field(
        ..., 
        alias="playerMicroformatRenderer", 
        description="Player microformat renderer data"
    )


class VideoDetailsResponse(BaseModel):
    """Complete YouTube video details API response."""
    
    video_details: VideoDetails = Field(..., alias="videoDetails", description="Core video details")
    microformat: Microformat = Field(..., description="Additional microformat metadata")
    
    class Config:
        """Pydantic configuration."""
        allow_population_by_field_name = True
        use_enum_values = True

# Load test data from JSON file
with open(r"C:\Users\Lucas\Documents\2. Areas\youtube_data_hoarder\YT_crawler\video_details.json", 'r') as f:
    test_data = json.load(f)

# Test with original data - works with both Pydantic v1 and v2
try:
    # Try Pydantic v2 first, fallback to v1
    try:
        instance = VideoDetailsResponse.model_validate(test_data)  # Pydantic v2
        print("Using Pydantic v2")
    except AttributeError:
        instance = VideoDetailsResponse.parse_obj(test_data)  # Pydantic v1
        print("Using Pydantic v1")
    
    print(f"Success: Model parsed correctly - {type(instance).__name__}")
    print("RESULT: PASS")
    
except Exception as e:
    print(f"Error: {str(e)}")
    print("RESULT: FAIL")
