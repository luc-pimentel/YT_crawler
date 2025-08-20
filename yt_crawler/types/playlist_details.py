"""
Pydantic models for YouTube scripts.json structure.

Generated from scripts.json structure containing playlist details with comprehensive 
type mapping, validation rules, and proper field definitions following project conventions.

This model represents YouTube playlist UI component data extracted from JavaScript
objects, including title rendering, metadata, logging context, and avatar stacks.
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any


class ClientVeSpec(BaseModel):
    """Client view event specification for tracking."""
    
    ui_type: int = Field(..., alias="uiType", description="UI component type identifier")
    ve_counter: int = Field(..., alias="veCounter", description="View event counter")


class Visibility(BaseModel):
    """Visibility configuration for tracking."""
    
    types: str = Field(..., description="Visibility type configuration")


class LoggingDirectives(BaseModel):
    """Logging directives for tracking and analytics."""
    
    tracking_params: str = Field(..., alias="trackingParams", description="Tracking parameters for analytics")
    visibility: Visibility = Field(..., description="Visibility configuration")
    client_ve_spec: ClientVeSpec = Field(..., alias="clientVeSpec", description="Client view event specification")


class LoggingContext(BaseModel):
    """Logging context container."""
    
    logging_directives: LoggingDirectives = Field(..., alias="loggingDirectives", description="Logging and tracking directives")


class RendererContext(BaseModel):
    """Renderer context for UI components."""
    
    logging_context: LoggingContext = Field(..., alias="loggingContext", description="Logging context for tracking")


class TextContent(BaseModel):
    """Text content container."""
    
    content: str = Field(..., description="Text content")


class DynamicTextViewModel(BaseModel):
    """Dynamic text view model for title rendering."""
    
    text: TextContent = Field(..., description="Text content")
    renderer_context: RendererContext = Field(..., alias="rendererContext", description="Renderer context")


class TitleContainer(BaseModel):
    """Title container with dynamic text view model."""
    
    dynamic_text_view_model: DynamicTextViewModel = Field(..., alias="dynamicTextViewModel", description="Dynamic text view model")


class ImageSource(BaseModel):
    """Image source with dimensions."""
    
    url: HttpUrl = Field(..., description="Image URL")
    width: int = Field(..., description="Image width in pixels")
    height: int = Field(..., description="Image height in pixels")


class BorderImageProcessor(BaseModel):
    """Border image processor configuration."""
    
    circular: bool = Field(..., description="Whether image should be circular")


class ImageProcessor(BaseModel):
    """Image processor configuration."""
    
    border_image_processor: BorderImageProcessor = Field(..., alias="borderImageProcessor", description="Border image processor")


class ImageContainer(BaseModel):
    """Image container with sources and processor."""
    
    sources: List[ImageSource] = Field(..., description="List of image sources with different sizes")
    processor: ImageProcessor = Field(..., description="Image processing configuration")


class WebCommandMetadata(BaseModel):
    """Web command metadata for navigation."""
    
    url: str = Field(..., description="Navigation URL")
    web_page_type: str = Field(..., alias="webPageType", description="Web page type")
    root_ve: int = Field(..., alias="rootVe", description="Root view event")
    api_url: str = Field(..., alias="apiUrl", description="API URL")


class CommandMetadata(BaseModel):
    """Command metadata container."""
    
    web_command_metadata: WebCommandMetadata = Field(..., alias="webCommandMetadata", description="Web command metadata")


class BrowseEndpoint(BaseModel):
    """Browse endpoint for channel navigation."""
    
    browse_id: str = Field(..., alias="browseId", description="Browse identifier")
    canonical_base_url: str = Field(..., alias="canonicalBaseUrl", description="Canonical base URL")


class InnertubeCommand(BaseModel):
    """Innertube command for navigation."""
    
    click_tracking_params: str = Field(..., alias="clickTrackingParams", description="Click tracking parameters")
    command_metadata: CommandMetadata = Field(..., alias="commandMetadata", description="Command metadata")
    browse_endpoint: BrowseEndpoint = Field(..., alias="browseEndpoint", description="Browse endpoint")


class OnTap(BaseModel):
    """On tap action configuration."""
    
    innertube_command: InnertubeCommand = Field(..., alias="innertubeCommand", description="Innertube command")


class CommandRun(BaseModel):
    """Command run for interactive text."""
    
    start_index: int = Field(..., alias="startIndex", description="Start index in text")
    length: int = Field(..., description="Length of command run")
    on_tap: OnTap = Field(..., alias="onTap", description="On tap action")


class StyleRun(BaseModel):
    """Style run for text formatting."""
    
    start_index: int = Field(..., alias="startIndex", description="Start index in text")
    length: int = Field(..., description="Length of style run")
    font_color: int = Field(..., alias="fontColor", description="Font color")
    weight_label: str = Field(..., alias="weightLabel", description="Font weight label")


class StackText(BaseModel):
    """Text with command and style runs."""
    
    content: str = Field(..., description="Text content")
    command_runs: List[CommandRun] = Field(..., alias="commandRuns", description="List of command runs")
    style_runs: List[StyleRun] = Field(..., alias="styleRuns", description="List of style runs")


class AccessibilityContext(BaseModel):
    """Accessibility context for UI components."""
    
    # This is truncated in the schema but would contain accessibility data
    pass


class AvatarStackRendererContext(BaseModel):
    """Renderer context for avatar stack."""
    
    logging_context: LoggingContext = Field(..., alias="loggingContext", description="Logging context")
    accessibility_context: Optional[AccessibilityContext] = Field(None, alias="accessibilityContext", description="Accessibility context")


class AvatarViewModel(BaseModel):
    """Avatar view model."""
    
    image: ImageContainer = Field(..., description="Avatar image")
    avatar_image_size: str = Field(..., alias="avatarImageSize", description="Avatar image size")


class Avatar(BaseModel):
    """Avatar container."""
    
    avatar_view_model: AvatarViewModel = Field(..., alias="avatarViewModel", description="Avatar view model")


class AvatarStackViewModel(BaseModel):
    """Avatar stack view model."""
    
    avatars: List[Avatar] = Field(..., description="List of avatars")
    text: StackText = Field(..., description="Stack text with formatting")
    renderer_context: AvatarStackRendererContext = Field(..., alias="rendererContext", description="Renderer context")


class AvatarStack(BaseModel):
    """Avatar stack container."""
    
    avatar_stack_view_model: AvatarStackViewModel = Field(..., alias="avatarStackViewModel", description="Avatar stack view model")


class SimpleText(BaseModel):
    """Simple text content."""
    
    content: str = Field(..., description="Text content")


class MetadataPart(BaseModel):
    """Metadata part container that can contain either avatar stack or simple text."""
    
    avatar_stack: Optional[AvatarStack] = Field(None, alias="avatarStack", description="Avatar stack (optional)")
    text: Optional[SimpleText] = Field(None, description="Simple text content (optional)")


class MetadataRow(BaseModel):
    """Metadata row container."""
    
    metadata_parts: List[MetadataPart] = Field(..., alias="metadataParts", description="List of metadata parts")


class ContentMetadataViewModel(BaseModel):
    """Content metadata view model."""
    
    metadata_rows: List[MetadataRow] = Field(..., alias="metadataRows", description="List of metadata rows")
    delimiter: str = Field(..., description="Metadata delimiter character")
    renderer_context: RendererContext = Field(..., alias="rendererContext", description="Renderer context")


class MetadataContainer(BaseModel):
    """Metadata container."""
    
    content_metadata_view_model: ContentMetadataViewModel = Field(..., alias="contentMetadataViewModel", description="Content metadata view model")


class PlaylistDetails(BaseModel):
    """YouTube playlist details with title and metadata."""
    
    title: TitleContainer = Field(..., description="Playlist title container")
    metadata: MetadataContainer = Field(..., description="Playlist metadata container")


class PlaylistDetailsResponse(BaseModel):
    """Response model for YouTube playlist details data structure.
    
    This model represents YouTube playlist UI component data extracted from JavaScript
    objects, containing structured information about playlist titles, metadata,
    creator information, and UI rendering contexts.
    """
    
    playlist_details: PlaylistDetails = Field(..., alias="playlist_details", description="Complete playlist details including title and metadata")
    
    class Config:
        """Pydantic configuration."""
        validate_by_name = True
        extra = "forbid"