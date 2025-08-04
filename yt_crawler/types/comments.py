"""
Pydantic models for YouTube video comments data.

Generated from video_comments.json structure with comprehensive type mapping,
validation rules, and proper field definitions.
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any


class CommentContent(BaseModel):
    """Comment text content."""
    
    content: str = Field(..., description="The actual comment text content")


class CommentProperties(BaseModel):
    """Core comment properties and metadata."""
    
    comment_id: str = Field(..., alias="commentId", description="Unique comment identifier")
    content: CommentContent = Field(..., description="Comment text content")
    published_time: str = Field(..., alias="publishedTime", description="Human-readable publication time (e.g., '1 year ago')")
    reply_level: int = Field(..., alias="replyLevel", description="Nesting level of the comment (0 for top-level)")
    author_button_a11y: str = Field(..., alias="authorButtonA11y", description="Author button accessibility text")
    toolbar_state_key: str = Field(..., alias="toolbarStateKey", description="Toolbar state identifier key")
    translate_button_entity_key: str = Field(..., alias="translateButtonEntityKey", description="Translation button entity key")


class InnertubeCommand(BaseModel):
    """Innertube command for navigation."""
    
    clickTrackingParams: Optional[str] = Field(None, description="Click tracking parameters")
    commandMetadata: Optional[Dict[str, Any]] = Field(None, description="Command metadata")
    browseEndpoint: Optional[Dict[str, Any]] = Field(None, description="Browse endpoint information")


class ChannelCommand(BaseModel):
    """Channel navigation command."""
    
    innertube_command: InnertubeCommand = Field(..., alias="innertubeCommand", description="Innertube navigation command")


class CommentAuthor(BaseModel):
    """Comment author information."""
    
    channel_id: str = Field(..., alias="channelId", description="Author's channel identifier")
    display_name: str = Field(..., alias="displayName", description="Author's display name")
    avatar_thumbnail_url: HttpUrl = Field(..., alias="avatarThumbnailUrl", description="Author's avatar thumbnail URL")
    is_verified: bool = Field(..., alias="isVerified", description="Whether the author is verified")
    is_current_user: bool = Field(..., alias="isCurrentUser", description="Whether this is the current user")
    is_creator: bool = Field(..., alias="isCreator", description="Whether the author is the video creator")
    channel_command: ChannelCommand = Field(..., alias="channelCommand", description="Channel navigation command")
    is_artist: bool = Field(..., alias="isArtist", description="Whether the author is an artist")


class EngagementToolbarStyle(BaseModel):
    """Engagement toolbar styling."""
    
    value: str = Field(..., description="Toolbar style value")


class CommentToolbar(BaseModel):
    """Comment interaction toolbar."""
    
    like_count_liked: str = Field(..., alias="likeCountLiked", description="Like count when comment is liked")
    like_count_not_liked: str = Field(..., alias="likeCountNotliked", description="Like count when comment is not liked")
    reply_count: str = Field(..., alias="replyCount", description="Number of replies to this comment")
    creator_thumbnail_url: Optional[HttpUrl] = Field(None, alias="creatorThumbnailUrl", description="Creator thumbnail URL")
    like_button_a11y: str = Field(..., alias="likeButtonA11y", description="Like button accessibility text")
    engagement_toolbar_style: EngagementToolbarStyle = Field(..., alias="engagementToolbarStyle", description="Toolbar styling")
    like_count_a11y: str = Field(..., alias="likeCountA11y", description="Like count accessibility text")
    reply_count_a11y: str = Field(..., alias="replyCountA11y", description="Reply count accessibility text")
    like_inactive_tooltip: str = Field(..., alias="likeInactiveTooltip", description="Like button inactive tooltip")
    like_active_tooltip: str = Field(..., alias="likeActiveTooltip", description="Like button active tooltip")
    dislike_inactive_tooltip: str = Field(..., alias="dislikeInactiveTooltip", description="Dislike button inactive tooltip")
    dislike_active_tooltip: str = Field(..., alias="dislikeActiveTooltip", description="Dislike button active tooltip")
    heart_active_tooltip: str = Field(..., alias="heartActiveTooltip", description="Heart button active tooltip")


class ImageSource(BaseModel):
    """Image source information."""
    
    url: HttpUrl = Field(..., description="Image source URL")
    width: Optional[int] = Field(None, description="Image width in pixels")
    height: Optional[int] = Field(None, description="Image height in pixels")


class AvatarImage(BaseModel):
    """Avatar image information."""
    
    sources: List[ImageSource] = Field(..., description="List of image sources")
    processor: Optional[Dict[str, Any]] = Field(None, description="Image processor information")


class AvatarEndpoint(BaseModel):
    """Avatar navigation endpoint."""
    
    innertube_command: InnertubeCommand = Field(..., alias="innertubeCommand", description="Innertube navigation command")


class CommentAvatar(BaseModel):
    """Comment author avatar."""
    
    image: AvatarImage = Field(..., description="Avatar image information")
    accessibility_text: str = Field(..., alias="accessibilityText", description="Avatar accessibility text")
    avatar_image_size: str = Field(..., alias="avatarImageSize", description="Avatar image size identifier")
    endpoint: AvatarEndpoint = Field(..., description="Avatar navigation endpoint")


class VisibilityInfo(BaseModel):
    """Visibility information."""
    
    types: str = Field(..., description="Visibility types")


class LoggingDirectivesInfo(BaseModel):
    """Logging directives information."""
    
    tracking_params: str = Field(..., alias="trackingParams", description="Tracking parameters")
    visibility: VisibilityInfo = Field(..., description="Visibility information")


class ReadMoreLogging(BaseModel):
    """Read more button logging information."""
    
    tracking_params: str = Field(..., alias="trackingParams", description="Tracking parameters for read more")
    logging_directives: LoggingDirectivesInfo = Field(..., alias="loggingDirectives", description="Logging directives")


class ClientVeSpec(BaseModel):
    """Client VE specification."""
    
    ui_type: str = Field(..., alias="uiType", description="UI type identifier")
    ve_counter: str = Field(..., alias="veCounter", description="VE counter")


class CommentLoggingDirectives(BaseModel):
    """Comment logging directives."""
    
    tracking_params: str = Field(..., alias="trackingParams", description="Tracking parameters")
    visibility: VisibilityInfo = Field(..., description="Visibility information")
    client_ve_spec: ClientVeSpec = Field(..., alias="clientVeSpec", description="Client VE specification")


class VideoComment(BaseModel):
    """Individual video comment with all metadata."""
    
    key: str = Field(..., description="Unique comment key identifier")
    properties: CommentProperties = Field(..., description="Core comment properties")
    author: CommentAuthor = Field(..., description="Comment author information")
    toolbar: CommentToolbar = Field(..., description="Comment interaction toolbar")
    avatar: CommentAvatar = Field(..., description="Author avatar information")
    read_more_logging: ReadMoreLogging = Field(..., alias="readMoreLogging", description="Read more button logging")
    logging_directives: CommentLoggingDirectives = Field(..., alias="loggingDirectives", description="Comment logging directives")


class VideoCommentsResponse(BaseModel):
    """Container for video comments response."""
    
    comments: List[VideoComment] = Field(..., description="List of video comments")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            HttpUrl: str
        }