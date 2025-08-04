from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime

# Import common types from search module
from .search import Thumbnail, TextWithRuns, SimpleText, NavigationEndpoint, Accessibility


class TrendingNewsTitle(BaseModel):
    """Title for trending news section."""
    simpleText: Optional[str] = Field(None, description="Simple text content for news section title")
    runs: Optional[List[Dict[str, Any]]] = Field(None, description="Text runs for formatted title")


class OwnerBadge(BaseModel):
    """Owner badge information."""
    metadataBadgeRenderer: Dict[str, Any] = Field(..., description="Metadata badge renderer data")


class ThumbnailOverlay(BaseModel):
    """Thumbnail overlay information."""
    thumbnailOverlayTimeStatusRenderer: Optional[Dict[str, Any]] = Field(None, description="Time status renderer")
    thumbnailOverlayToggleButtonRenderer: Optional[Dict[str, Any]] = Field(None, description="Toggle button renderer")
    thumbnailOverlayNowPlayingRenderer: Optional[Dict[str, Any]] = Field(None, description="Now playing renderer")
    thumbnailOverlayLoadingPreviewRenderer: Optional[Dict[str, Any]] = Field(None, description="Loading preview renderer")


class RichThumbnail(BaseModel):
    """Rich thumbnail with moving preview."""
    movingThumbnailRenderer: Dict[str, Any] = Field(..., description="Moving thumbnail renderer data")


class Avatar(BaseModel):
    """Channel avatar information."""
    decoratedAvatarViewModel: Dict[str, Any] = Field(..., description="Decorated avatar view model")


class ChannelThumbnailRenderer(BaseModel):
    """Channel thumbnail renderer."""
    thumbnail: Thumbnail = Field(..., description="Channel thumbnail data")
    navigationEndpoint: NavigationEndpoint = Field(..., description="Navigation endpoint for channel")
    accessibility: Accessibility = Field(..., description="Accessibility information")


class ChannelThumbnailSupportedRenderers(BaseModel):
    """Supported channel thumbnail renderers."""
    channelThumbnailWithLinkRenderer: ChannelThumbnailRenderer = Field(..., description="Channel thumbnail with link renderer")


class Menu(BaseModel):
    """Video menu information."""
    menuRenderer: Dict[str, Any] = Field(..., description="Menu renderer data")


class VideoRenderer(BaseModel):
    """Video renderer containing all video metadata."""
    videoId: str = Field(..., description="YouTube video ID")
    thumbnail: Thumbnail = Field(..., description="Video thumbnail information")
    title: TextWithRuns = Field(..., description="Video title with runs and accessibility")
    descriptionSnippet: Optional[TextWithRuns] = Field(None, description="Video description snippet")
    longBylineText: TextWithRuns = Field(..., description="Long byline text (channel name)")
    publishedTimeText: Optional[SimpleText] = Field(None, description="Published time text (optional for live streams)")
    lengthText: Optional[SimpleText] = Field(None, description="Video length text (optional for live streams)")
    viewCountText: SimpleText = Field(..., description="View count text")
    navigationEndpoint: NavigationEndpoint = Field(..., description="Navigation endpoint for video")
    ownerBadges: Optional[List[OwnerBadge]] = Field(None, description="Owner badges (e.g., verified)")
    ownerText: TextWithRuns = Field(..., description="Owner/channel text")
    shortBylineText: TextWithRuns = Field(..., description="Short byline text")
    trackingParams: str = Field(..., description="Tracking parameters")
    showActionMenu: bool = Field(..., description="Whether to show action menu")
    shortViewCountText: SimpleText = Field(..., description="Short view count text")
    menu: Menu = Field(..., description="Video menu")
    channelThumbnailSupportedRenderers: ChannelThumbnailSupportedRenderers = Field(..., description="Channel thumbnail renderers")
    thumbnailOverlays: List[ThumbnailOverlay] = Field(..., description="Thumbnail overlays")
    richThumbnail: Optional[RichThumbnail] = Field(None, description="Rich thumbnail with preview")
    avatar: Optional[Avatar] = Field(None, description="Channel avatar")


class ContentRenderer(BaseModel):
    """Content renderer container."""
    videoRenderer: VideoRenderer = Field(..., description="Video renderer data")


class RichItemRenderer(BaseModel):
    """Rich item renderer containing content and tracking."""
    content: ContentRenderer = Field(..., description="Content renderer")
    trackingParams: str = Field(..., description="Tracking parameters for the item")


class TrendingNewsContent(BaseModel):
    """Individual content item in trending news."""
    richItemRenderer: RichItemRenderer = Field(..., description="Rich item renderer")


class ButtonIcon(BaseModel):
    """Button icon information."""
    iconType: str = Field(..., description="Icon type identifier")


class ButtonAccessibility(BaseModel):
    """Button accessibility information."""
    label: str = Field(..., description="Accessibility label for button")


class ButtonRenderer(BaseModel):
    """Button renderer for show more/less buttons."""
    style: str = Field(..., description="Button style")
    size: str = Field(..., description="Button size")
    text: TextWithRuns = Field(..., description="Button text")
    icon: ButtonIcon = Field(..., description="Button icon")
    accessibility: ButtonAccessibility = Field(..., description="Button accessibility")
    trackingParams: str = Field(..., description="Button tracking parameters")


class ShowMoreButton(BaseModel):
    """Show more button container."""
    buttonRenderer: ButtonRenderer = Field(..., description="Button renderer")


class ShowLessButton(BaseModel):
    """Show less button container."""
    buttonRenderer: ButtonRenderer = Field(..., description="Button renderer")


class ResponsiveContainerConfiguration(BaseModel):
    """Responsive container configuration."""
    # This can be a flexible dict since the structure may vary
    pass


class TrendingNewsSection(BaseModel):
    """Individual trending news section."""
    title: TrendingNewsTitle = Field(..., description="Section title")
    contents: List[TrendingNewsContent] = Field(..., description="List of news content items")
    trackingParams: str = Field(..., description="Tracking parameters for the section")
    showMoreButton: ShowMoreButton = Field(..., description="Show more button")
    isExpanded: bool = Field(..., description="Whether section is expanded")
    isTopDividerHidden: bool = Field(..., alias="isTopDividerHidden", description="Whether top divider is hidden")
    isBottomDividerHidden: bool = Field(..., alias="isBottomDividerHidden", description="Whether bottom divider is hidden") 
    showLessButton: Optional[ShowLessButton] = Field(None, description="Show less button")
    responsiveContainerConfiguration: Optional[Dict[str, Any]] = Field(None, description="Responsive container configuration")


class TrendingNewsResponse(BaseModel):
    """Root response model for trending news data."""
    trending_news: List[TrendingNewsSection] = Field(..., description="List of trending news sections")

    class Config:
        """Pydantic configuration."""
        allow_population_by_field_name = True
        use_enum_values = True


# Export main models
__all__ = [
    "TrendingNewsTitle",
    "OwnerBadge", 
    "ThumbnailOverlay",
    "RichThumbnail",
    "Avatar",
    "ChannelThumbnailRenderer",
    "ChannelThumbnailSupportedRenderers",
    "Menu",
    "VideoRenderer",
    "ContentRenderer",
    "RichItemRenderer", 
    "TrendingNewsContent",
    "ButtonIcon",
    "ButtonAccessibility",
    "ButtonRenderer",
    "ShowMoreButton",
    "ShowLessButton",
    "TrendingNewsSection",
    "TrendingNewsResponse",
]