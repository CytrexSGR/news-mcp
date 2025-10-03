"""
Pydantic schemas for Content Distribution System.

These schemas define the API request/response structures for:
- Content Templates
- Generated Content
- Distribution Channels
- Distribution Logs
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field, ConfigDict


# ===== Template Schemas =====

class SelectionCriteria(BaseModel):
    """Criteria for selecting articles to include in content generation."""

    keywords: Optional[List[str]] = Field(None, description="Keywords to search for (OR condition)")
    exclude_keywords: Optional[List[str]] = Field(None, description="Keywords to exclude")
    timeframe_hours: Optional[int] = Field(None, description="Look back N hours from now", ge=1)
    min_impact_score: Optional[float] = Field(None, description="Minimum impact score", ge=0.0, le=1.0)
    min_sentiment_score: Optional[float] = Field(None, description="Minimum sentiment score", ge=-1.0, le=1.0)
    feed_ids: Optional[List[int]] = Field(None, description="Filter by specific feed IDs")
    category_names: Optional[List[str]] = Field(None, description="Filter by category names")
    source_names: Optional[List[str]] = Field(None, description="Filter by source names")
    max_articles: int = Field(50, description="Maximum articles to include", ge=1, le=500)

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "keywords": ["security", "breach", "vulnerability"],
            "exclude_keywords": ["opinion"],
            "timeframe_hours": 24,
            "min_impact_score": 0.7,
            "feed_ids": [1, 5, 12],
            "max_articles": 30
        }
    })


class ContentSection(BaseModel):
    """Definition of a content section."""

    name: str = Field(..., description="Section identifier (e.g., 'executive_summary')")
    prompt: str = Field(..., description="LLM prompt for this section")
    max_words: Optional[int] = Field(None, description="Maximum words for this section", ge=10)
    max_items: Optional[int] = Field(None, description="Maximum list items (if format=list)", ge=1)
    format: Literal["paragraph", "list", "table"] = Field("paragraph", description="Output format")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "executive_summary",
            "prompt": "Provide a concise executive summary in 2-3 sentences",
            "max_words": 150,
            "format": "paragraph"
        }
    })


class ContentStructure(BaseModel):
    """Structure definition for generated content."""

    sections: List[ContentSection] = Field(..., description="Ordered list of content sections")
    output_format: Literal["markdown", "html", "json"] = Field("markdown", description="Final output format")
    include_source_links: bool = Field(True, description="Include links to source articles")
    include_metadata: bool = Field(True, description="Include generation metadata")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "sections": [
                {
                    "name": "summary",
                    "prompt": "Summarize key developments",
                    "max_words": 150,
                    "format": "paragraph"
                },
                {
                    "name": "alerts",
                    "prompt": "List critical alerts",
                    "max_items": 5,
                    "format": "list"
                }
            ],
            "output_format": "markdown",
            "include_source_links": True
        }
    })


class ContentTemplateBase(BaseModel):
    """Base template fields."""

    name: str = Field(..., description="Template name (unique)", min_length=3, max_length=200)
    description: Optional[str] = Field(None, description="Template description")
    target_audience: Optional[str] = Field(None, description="Target audience", max_length=100)
    selection_criteria: SelectionCriteria = Field(..., description="Article selection criteria")
    content_structure: ContentStructure = Field(..., description="Content structure definition")
    llm_prompt_template: str = Field(..., description="Base LLM prompt template", min_length=10)
    llm_model: str = Field("gpt-4o-mini", description="OpenAI model to use")
    llm_temperature: float = Field(0.7, description="LLM temperature", ge=0.0, le=2.0)
    generation_schedule: Optional[str] = Field(None, description="Cron expression or 'on_demand'")
    is_active: bool = Field(True, description="Is template active")
    tags: Optional[Dict[str, Any]] = Field(None, description="Optional metadata tags")


class ContentTemplateCreate(ContentTemplateBase):
    """Schema for creating a new template."""
    pass


class ContentTemplateUpdate(BaseModel):
    """Schema for updating a template (all fields optional)."""

    name: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None
    target_audience: Optional[str] = Field(None, max_length=100)
    selection_criteria: Optional[SelectionCriteria] = None
    content_structure: Optional[ContentStructure] = None
    llm_prompt_template: Optional[str] = Field(None, min_length=10)
    llm_model: Optional[str] = None
    llm_temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    generation_schedule: Optional[str] = None
    is_active: Optional[bool] = None
    tags: Optional[Dict[str, Any]] = None


class ContentTemplate(ContentTemplateBase):
    """Complete template response schema."""

    id: int
    created_at: datetime
    updated_at: datetime
    version: int

    model_config = ConfigDict(from_attributes=True)


class ContentTemplatePreview(BaseModel):
    """Preview of template selection results (test mode)."""

    template_id: int
    matching_articles_count: int
    sample_article_ids: List[int]
    estimated_cost_usd: float
    estimated_time_seconds: int
    articles_summary: List[Dict[str, Any]]  # Sample of matched articles

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "template_id": 1,
            "matching_articles_count": 18,
            "sample_article_ids": [1234, 1235, 1236],
            "estimated_cost_usd": 0.025,
            "estimated_time_seconds": 8,
            "articles_summary": [
                {
                    "id": 1234,
                    "title": "Critical OpenSSL vulnerability discovered",
                    "impact_score": 0.95,
                    "published_at": "2025-10-02T08:30:00Z"
                }
            ]
        }
    })


# ===== Generated Content Schemas =====

class GeneratedContentBase(BaseModel):
    """Base generated content fields."""

    template_id: int
    title: Optional[str] = Field(None, max_length=500)
    content_html: Optional[str] = None
    content_markdown: Optional[str] = None
    content_json: Optional[Dict[str, Any]] = None
    source_article_ids: List[int]
    articles_count: int
    word_count: Optional[int] = None
    generation_cost_usd: Optional[float] = None
    generation_time_seconds: Optional[int] = None
    llm_model_used: Optional[str] = None
    status: Literal["generated", "published", "archived", "failed"] = "generated"
    error_message: Optional[str] = None


class GeneratedContentCreate(BaseModel):
    """Schema for creating generated content (internal use)."""

    template_id: int
    title: Optional[str] = None
    content_html: Optional[str] = None
    content_markdown: Optional[str] = None
    content_json: Optional[Dict[str, Any]] = None
    source_article_ids: List[int]
    articles_count: int
    generation_job_id: Optional[str] = None
    word_count: Optional[int] = None
    generation_cost_usd: Optional[float] = None
    generation_time_seconds: Optional[int] = None
    llm_model_used: Optional[str] = None


class GeneratedContent(GeneratedContentBase):
    """Complete generated content response schema."""

    id: int
    generated_at: datetime
    published_at: Optional[datetime] = None
    generation_job_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class GeneratedContentSummary(BaseModel):
    """Lightweight summary for list views."""

    id: int
    template_id: int
    template_name: str
    title: Optional[str]
    status: str
    generated_at: datetime
    articles_count: int
    word_count: Optional[int]
    generation_cost_usd: Optional[float]

    model_config = ConfigDict(from_attributes=True)


# ===== Distribution Channel Schemas =====

class EmailChannelConfig(BaseModel):
    """Configuration for email distribution channel."""

    recipients: List[str] = Field(..., description="Email addresses", min_length=1)
    subject_template: str = Field(..., description="Email subject template (supports {date} variable)")
    from_address: str = Field("briefings@news-mcp.com", description="Sender email address")
    reply_to: Optional[str] = None

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "recipients": ["team@example.com", "manager@example.com"],
            "subject_template": "Daily Security Brief - {date}",
            "from_address": "security@news-mcp.com"
        }
    })


class WebChannelConfig(BaseModel):
    """Configuration for web publication channel."""

    publish_url_template: str = Field(..., description="URL template (supports {template_name}, {date})")
    access_control: Literal["public", "private", "api_key"] = Field("public", description="Access control type")
    auto_archive_days: Optional[int] = Field(None, description="Auto-archive after N days", ge=1)

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "publish_url_template": "/briefings/{template_name}/{date}",
            "access_control": "public",
            "auto_archive_days": 30
        }
    })


class RSSChannelConfig(BaseModel):
    """Configuration for RSS feed channel."""

    feed_url: str = Field(..., description="RSS feed URL")
    feed_title: str = Field(..., description="RSS feed title")
    feed_description: Optional[str] = None
    max_items: int = Field(50, description="Max items in feed", ge=1, le=100)

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "feed_url": "/feeds/security-brief.xml",
            "feed_title": "Security Intelligence Brief",
            "feed_description": "Daily security briefing for IT professionals",
            "max_items": 30
        }
    })


class APIChannelConfig(BaseModel):
    """Configuration for API webhook channel."""

    webhook_url: str = Field(..., description="Webhook endpoint URL")
    auth_token: Optional[str] = Field(None, description="Bearer token for authentication")
    custom_headers: Optional[Dict[str, str]] = None

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "webhook_url": "https://api.example.com/briefings",
            "auth_token": "Bearer sk-...",
            "custom_headers": {"X-Custom": "value"}
        }
    })


class DistributionChannelBase(BaseModel):
    """Base distribution channel fields."""

    template_id: int
    channel_type: Literal["email", "web", "rss", "api"]
    channel_name: str = Field(..., max_length=200)
    channel_config: Dict[str, Any]  # Union of config types
    is_active: bool = True


class DistributionChannelCreate(DistributionChannelBase):
    """Schema for creating a distribution channel."""
    pass


class DistributionChannelUpdate(BaseModel):
    """Schema for updating a distribution channel."""

    channel_name: Optional[str] = Field(None, max_length=200)
    channel_config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class DistributionChannel(DistributionChannelBase):
    """Complete distribution channel response schema."""

    id: int
    created_at: datetime
    last_used_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ===== Distribution Log Schemas =====

class DistributionLogBase(BaseModel):
    """Base distribution log fields."""

    content_id: int
    channel_id: int
    status: Literal["pending", "sent", "failed", "retry"] = "pending"
    recipient_count: Optional[int] = None
    error_message: Optional[str] = None


class DistributionLogCreate(DistributionLogBase):
    """Schema for creating a distribution log entry."""
    pass


class DistributionLog(DistributionLogBase):
    """Complete distribution log response schema."""

    id: int
    sent_at: Optional[datetime] = None
    retry_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ===== Content Generation Request/Response =====

class ContentGenerationRequest(BaseModel):
    """Request to generate content."""

    template_id: int
    async_mode: bool = Field(True, description="Queue for async processing (true) or wait for sync result (false)")
    force_regenerate: bool = Field(False, description="Regenerate even if recent content exists")


class ContentGenerationResponse(BaseModel):
    """Response from content generation request."""

    success: bool
    job_id: Optional[str] = None
    status: Literal["queued", "processing", "completed", "failed"]
    message: str
    content_id: Optional[int] = None
    content: Optional[GeneratedContent] = None  # Only for sync mode

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "success": True,
            "job_id": "abc-123-def",
            "status": "queued",
            "message": "Content generation queued successfully"
        }
    })


class DistributionRequest(BaseModel):
    """Request to distribute content."""

    content_id: int
    channel_ids: Optional[List[int]] = Field(None, description="Specific channels (null = all active)")


class DistributionResponse(BaseModel):
    """Response from distribution request."""

    success: bool
    distribution_jobs: List[Dict[str, Any]]
    message: str

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "success": True,
            "distribution_jobs": [
                {
                    "channel_id": 1,
                    "channel_name": "IT Team Email",
                    "status": "sent",
                    "recipients": 5
                },
                {
                    "channel_id": 2,
                    "channel_name": "Web Publication",
                    "status": "sent",
                    "url": "/briefings/security/2025-10-02"
                }
            ],
            "message": "Content distributed successfully to 2 channels"
        }
    })
