from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime

class ThumbnailInfo(BaseModel):
    """Individual thumbnail information."""
    url: HttpUrl = Field(..., description="Thumbnail image URL")
    width: int = Field(..., description="Thumbnail width in pixels")
    height: int = Field(..., description="Thumbnail height in pixels")

class Thumbnail(BaseModel):
    """Container for video thumbnails."""
    thumbnails: List[ThumbnailInfo] = Field(..., description="List of available thumbnails")

class TextRun(BaseModel):
    """Text run with potential navigation endpoint."""
    text: str = Field(..., description="Display text")
    navigationEndpoint: Optional[Dict[str, Any]] = Field(None, description="Navigation metadata")

class AccessibilityData(BaseModel):
    """Accessibility information."""
    label: str = Field(..., description="Accessibility label")

class Accessibility(BaseModel):
    """Container for accessibility data."""
    accessibilityData: AccessibilityData = Field(..., description="Accessibility information")

class TextWithRuns(BaseModel):
    """Text container with runs and accessibility."""
    runs: List[TextRun] = Field(..., description="Text runs")
    accessibility: Optional[Accessibility] = Field(None, description="Accessibility information")

class SimpleText(BaseModel):
    """Simple text container."""
    simpleText: Optional[str] = Field(None, description="Simple text content")
    runs: Optional[List[TextRun]] = Field(None, description="Text runs (alternative to simpleText)")
    accessibility: Optional[Accessibility] = Field(None, description="Accessibility information")

class LengthText(BaseModel):
    """Video length text with accessibility."""
    accessibility: Accessibility = Field(..., description="Accessibility information for length")  
    simpleText: str = Field(..., description="Video length (e.g., '4:24')")

class WebCommandMetadata(BaseModel):
    """Web command metadata."""
    url: str = Field(..., description="Target URL")
    webPageType: str = Field(..., description="Page type identifier")
    rootVe: int = Field(..., description="Root VE identifier")
    apiUrl: Optional[str] = Field(None, description="API URL")

class CommandMetadata(BaseModel):
    """Command metadata container."""
    webCommandMetadata: WebCommandMetadata = Field(..., description="Web command metadata")

class BrowseEndpoint(BaseModel):
    """Browse endpoint for channel navigation."""
    browseId: str = Field(..., description="YouTube channel ID")
    canonicalBaseUrl: str = Field(..., description="Canonical base URL")

class VssLoggingContext(BaseModel):
    """VSS logging context."""
    serializedContextData: str = Field(..., description="Serialized context data")

class LoggingContext(BaseModel):
    """Logging context container."""
    vssLoggingContext: VssLoggingContext = Field(..., description="VSS logging context")

class CommonConfig(BaseModel):
    """Common configuration."""
    url: HttpUrl = Field(..., description="Configuration URL")

class Html5PlaybackOnesieConfig(BaseModel):
    """HTML5 playback configuration."""
    commonConfig: CommonConfig = Field(..., description="Common configuration")

class WatchEndpointSupportedOnesieConfig(BaseModel):
    """Watch endpoint configuration."""
    html5PlaybackOnesieConfig: Html5PlaybackOnesieConfig = Field(..., description="HTML5 playback config")

class WatchEndpoint(BaseModel):
    """Watch endpoint for video playback."""
    videoId: str = Field(..., description="YouTube video ID")
    playlistId: Optional[str] = Field(None, description="YouTube playlist ID")
    params: Optional[str] = Field(None, description="Encoded parameters")
    playerParams: Optional[str] = Field(None, description="Player parameters")
    loggingContext: Optional[LoggingContext] = Field(None, description="Logging context")
    watchEndpointSupportedOnesieConfig: Optional[WatchEndpointSupportedOnesieConfig] = Field(None, description="Onesie config")

class NavigationEndpoint(BaseModel):
    """Navigation endpoint with tracking and commands."""
    clickTrackingParams: str = Field(..., description="Click tracking parameters")
    commandMetadata: CommandMetadata = Field(..., description="Command metadata")
    watchEndpoint: Optional[WatchEndpoint] = Field(None, description="Watch endpoint for videos")
    browseEndpoint: Optional[BrowseEndpoint] = Field(None, description="Browse endpoint for channels")

class IconInfo(BaseModel):
    """Icon information."""
    iconType: str = Field(..., description="Icon type identifier")

class MetadataBadgeRenderer(BaseModel):
    """Metadata badge renderer."""
    icon: IconInfo = Field(..., description="Badge icon")
    style: str = Field(..., description="Badge style")
    tooltip: str = Field(..., description="Badge tooltip")
    trackingParams: str = Field(..., description="Tracking parameters")
    accessibilityData: AccessibilityData = Field(..., description="Accessibility data")

class OwnerBadge(BaseModel):
    """Owner badge information."""
    metadataBadgeRenderer: MetadataBadgeRenderer = Field(..., description="Badge renderer")

class SearchResult(BaseModel):
    """Individual search result video."""
    videoId: str = Field(..., description="YouTube video ID")
    thumbnail: Thumbnail = Field(..., description="Video thumbnail information")
    title: TextWithRuns = Field(..., description="Video title with runs")
    longBylineText: TextWithRuns = Field(..., description="Long byline text (channel info)")
    publishedTimeText: Optional[SimpleText] = Field(None, description="Published time text")
    lengthText: Optional[LengthText] = Field(None, description="Video length information (not present for live streams)")
    viewCountText: SimpleText = Field(..., description="View count text")
    navigationEndpoint: NavigationEndpoint = Field(..., description="Navigation endpoint")
    ownerBadges: Optional[List[OwnerBadge]] = Field(None, description="Owner badges (e.g., verified)")
    ownerText: TextWithRuns = Field(..., description="Owner/channel text")
    shortBylineText: TextWithRuns = Field(..., description="Short byline text")
    trackingParams: str = Field(..., description="Tracking parameters")
    showActionMenu: bool = Field(..., description="Show action menu flag")
    shortViewCountText: SimpleText = Field(..., description="Short view count text")
    menu: Dict[str, Any] = Field(..., description="Video menu configuration")
    channelThumbnailSupportedRenderers: Dict[str, Any] = Field(..., description="Channel thumbnail renderers")
    thumbnailOverlays: List[Dict[str, Any]] = Field(..., description="Thumbnail overlays")
    detailedMetadataSnippets: Optional[List[Dict[str, Any]]] = Field(None, description="Detailed metadata snippets")
    inlinePlaybackEndpoint: Optional[Dict[str, Any]] = Field(None, description="Inline playback endpoint")
    searchVideoResultEntityKey: str = Field(..., description="Search video result entity key")

class SearchResultsModel(BaseModel):
    """Complete search results container."""
    search_results: List[SearchResult] = Field(..., description="List of search results")

    class Config:
        """Pydantic configuration."""
        extra = "forbid"
        validate_assignment = True
