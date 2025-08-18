"""
Pydantic models for YouTube playlist videos API response.

Generated from playlist_videos.json structure with comprehensive type mapping,
validation rules, and proper field definitions following project conventions.
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any


class ThumbnailItem(BaseModel):
    """Individual thumbnail image with dimensions."""
    
    url: HttpUrl = Field(..., description="Direct URL to the thumbnail image")
    width: int = Field(..., description="Thumbnail width in pixels")
    height: int = Field(..., description="Thumbnail height in pixels")


class ThumbnailContainer(BaseModel):
    """Container for video thumbnails."""
    
    thumbnails: List[ThumbnailItem] = Field(..., description="List of available thumbnail sizes")


class AccessibilityData(BaseModel):
    """Accessibility information."""
    
    label: str = Field(..., description="Accessibility label text")


class Accessibility(BaseModel):
    """Container for accessibility data."""
    
    accessibilityData: AccessibilityData = Field(..., description="Accessibility information")


class TextRun(BaseModel):
    """Text run with optional navigation endpoint."""
    
    text: str = Field(..., description="Display text content")
    navigationEndpoint: Optional[Dict[str, Any]] = Field(None, description="Navigation metadata for clickable text")


class TextWithRuns(BaseModel):
    """Text container with runs and accessibility."""
    
    runs: List[TextRun] = Field(..., description="List of text runs")
    accessibility: Optional[Accessibility] = Field(None, description="Accessibility information")


class SimpleTextContainer(BaseModel):
    """Simple text container with accessibility."""
    
    simpleText: str = Field(..., description="Simple text content")


class IndexContainer(BaseModel):
    """Container for playlist index."""
    
    simpleText: str = Field(..., description="Playlist index as string (e.g., '1')")


class LengthText(BaseModel):
    """Video length text with accessibility."""
    
    accessibility: Accessibility = Field(..., description="Accessibility information for length")
    simpleText: str = Field(..., description="Video duration (e.g., '7:38')")


class WebCommandMetadata(BaseModel):
    """Web command metadata."""
    
    url: str = Field(..., description="Target URL")
    webPageType: str = Field(..., description="Page type identifier")
    rootVe: int = Field(..., description="Root VE identifier")


class CommandMetadata(BaseModel):
    """Command metadata container."""
    
    webCommandMetadata: WebCommandMetadata = Field(..., description="Web command metadata")


class BrowseEndpoint(BaseModel):
    """Browse endpoint for channel navigation."""
    
    browseId: str = Field(..., description="YouTube channel ID")
    canonicalBaseUrl: str = Field(..., description="Canonical channel URL")


class VssLoggingContext(BaseModel):
    """VSS logging context."""
    
    serializedContextData: str = Field(..., description="Serialized context data")


class LoggingContext(BaseModel):
    """Logging context container."""
    
    vssLoggingContext: VssLoggingContext = Field(..., description="VSS logging context")


class CommonConfig(BaseModel):
    """Common configuration for playback."""
    
    url: HttpUrl = Field(..., description="Configuration URL")


class Html5PlaybackOnesieConfig(BaseModel):
    """HTML5 playback configuration."""
    
    commonConfig: CommonConfig = Field(..., description="Common configuration")


class WatchEndpointSupportedOnesieConfig(BaseModel):
    """Watch endpoint supported configuration."""
    
    html5PlaybackOnesieConfig: Html5PlaybackOnesieConfig = Field(..., description="HTML5 playback configuration")


class WatchEndpoint(BaseModel):
    """Watch endpoint for video playback."""
    
    videoId: str = Field(..., description="YouTube video ID")
    playlistId: str = Field(..., description="YouTube playlist ID")
    index: int = Field(..., description="Video index in playlist")
    params: str = Field(..., description="Encoded parameters")
    playerParams: str = Field(..., description="Player parameters")
    loggingContext: LoggingContext = Field(..., description="Logging context")
    watchEndpointSupportedOnesieConfig: WatchEndpointSupportedOnesieConfig = Field(..., description="Supported configuration")


class NavigationEndpoint(BaseModel):
    """Navigation endpoint with tracking and commands."""
    
    clickTrackingParams: str = Field(..., description="Click tracking parameters")
    commandMetadata: CommandMetadata = Field(..., description="Command metadata")
    watchEndpoint: Optional[WatchEndpoint] = Field(None, description="Watch endpoint for video playback")
    browseEndpoint: Optional[BrowseEndpoint] = Field(None, description="Browse endpoint for channel navigation")


class MenuServiceItemRenderer(BaseModel):
    """Menu service item renderer."""
    
    text: Optional[Dict[str, Any]] = Field(None, description="Menu item text")
    icon: Optional[Dict[str, Any]] = Field(None, description="Menu item icon")
    serviceEndpoint: Dict[str, Any] = Field(..., description="Service endpoint")
    trackingParams: str = Field(..., description="Tracking parameters")
    hasSeparator: Optional[bool] = Field(None, description="Has separator flag")


class MenuServiceItemDownloadRenderer(BaseModel):
    """Menu service item download renderer."""
    
    serviceEndpoint: Dict[str, Any] = Field(..., description="Download service endpoint")
    trackingParams: str = Field(..., description="Tracking parameters")


class MenuItem(BaseModel):
    """Individual menu item."""
    
    menuServiceItemRenderer: Optional[MenuServiceItemRenderer] = Field(None, description="Menu service item renderer")
    menuServiceItemDownloadRenderer: Optional[MenuServiceItemDownloadRenderer] = Field(None, description="Download menu item renderer")


class MenuRenderer(BaseModel):
    """Menu renderer for video actions."""
    
    items: List[MenuItem] = Field(..., description="List of menu items")
    trackingParams: str = Field(..., description="Menu tracking parameters")
    accessibility: Accessibility = Field(..., description="Menu accessibility information")


class MenuContainer(BaseModel):
    """Container for video menu."""
    
    menuRenderer: MenuRenderer = Field(..., description="Menu renderer")


class ThumbnailOverlayTimeStatusRenderer(BaseModel):
    """Thumbnail overlay for time status."""
    
    text: Dict[str, Any] = Field(..., description="Time status text")
    style: str = Field(..., description="Overlay style")


class ThumbnailOverlay(BaseModel):
    """Individual thumbnail overlay."""
    
    thumbnailOverlayTimeStatusRenderer: Optional[ThumbnailOverlayTimeStatusRenderer] = Field(None, description="Time status renderer")


class VideoInfo(BaseModel):
    """Video information runs."""
    
    runs: List[TextRun] = Field(..., description="Video information text runs")


class PlaylistVideoRenderer(BaseModel):
    """Individual playlist video renderer containing all video metadata."""
    
    videoId: str = Field(..., description="YouTube video ID")
    thumbnail: ThumbnailContainer = Field(..., description="Video thumbnail information")
    title: TextWithRuns = Field(..., description="Video title with text runs")
    index: IndexContainer = Field(..., description="Video index in playlist")
    shortBylineText: TextWithRuns = Field(..., description="Short byline text (channel name)")
    lengthText: LengthText = Field(..., description="Video duration information")
    navigationEndpoint: NavigationEndpoint = Field(..., description="Navigation endpoint for video")
    lengthSeconds: str = Field(..., description="Video duration in seconds as string")
    trackingParams: str = Field(..., description="Tracking parameters")
    isPlayable: bool = Field(..., description="Whether the video is playable")
    menu: MenuContainer = Field(..., description="Video action menu")
    thumbnailOverlays: List[ThumbnailOverlay] = Field(..., description="Thumbnail overlays")
    videoInfo: VideoInfo = Field(..., description="Video information")


class PlaylistVideoItem(BaseModel):
    """Individual playlist video item wrapper."""
    
    playlistVideoRenderer: PlaylistVideoRenderer = Field(..., description="Playlist video renderer")


class PlaylistVideosResponse(BaseModel):
    """Complete playlist videos response."""
    
    playlist_videos: List[PlaylistVideoItem] = Field(..., description="List of playlist video items")

    class Config:
        """Pydantic configuration."""
        extra = "forbid"
        validate_assignment = True