"""
API endpoints for Content Distribution management.

Provides endpoints to manage distribution channels and trigger content distribution.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

from app.database import get_session
from app.models.content_distribution import (
    DistributionChannel,
    DistributionLog,
    GeneratedContent,
    ContentTemplate,
)
from app.schemas.content_distribution import (
    DistributionChannelCreate,
    DistributionChannelUpdate,
    DistributionChannel as DistributionChannelSchema,
    DistributionLog as DistributionLogSchema,
    DistributionRequest,
    DistributionResponse,
)

router = APIRouter(prefix="/distribution", tags=["distribution"])


@router.post("/channels/", response_model=DistributionChannelSchema, status_code=201)
async def create_distribution_channel(
    channel_data: DistributionChannelCreate,
    session: Session = Depends(get_session)
):
    """
    Create a new distribution channel for a template.

    Args:
        channel_data: Channel configuration
        session: Database session

    Returns:
        Created distribution channel

    Raises:
        HTTPException: If template not found or duplicate channel exists
    """
    # Verify template exists
    template = session.get(ContentTemplate, channel_data.template_id)
    if not template:
        raise HTTPException(
            status_code=404,
            detail=f"Template with ID {channel_data.template_id} not found"
        )

    # Check for duplicate channel (same template + type + name)
    existing = session.exec(
        select(DistributionChannel).where(
            DistributionChannel.template_id == channel_data.template_id,
            DistributionChannel.channel_type == channel_data.channel_type,
            DistributionChannel.channel_name == channel_data.channel_name,
        )
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Distribution channel '{channel_data.channel_name}' of type '{channel_data.channel_type}' already exists for this template"
        )

    # Create channel
    channel = DistributionChannel(
        template_id=channel_data.template_id,
        channel_type=channel_data.channel_type,
        channel_name=channel_data.channel_name,
        channel_config=channel_data.channel_config,
        is_active=channel_data.is_active,
    )

    session.add(channel)
    session.commit()
    session.refresh(channel)

    return channel


@router.get("/channels/", response_model=List[DistributionChannelSchema])
async def list_distribution_channels(
    template_id: Optional[int] = Query(None, description="Filter by template ID"),
    channel_type: Optional[str] = Query(None, description="Filter by channel type"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    session: Session = Depends(get_session)
):
    """
    List distribution channels.

    Args:
        template_id: Filter by template ID (optional)
        channel_type: Filter by channel type (optional)
        is_active: Filter by active status (optional)
        skip: Number of records to skip
        limit: Maximum records to return
        session: Database session

    Returns:
        List of distribution channels
    """
    query = select(DistributionChannel).order_by(DistributionChannel.created_at.desc())

    if template_id is not None:
        query = query.where(DistributionChannel.template_id == template_id)

    if channel_type:
        query = query.where(DistributionChannel.channel_type == channel_type)

    if is_active is not None:
        query = query.where(DistributionChannel.is_active == is_active)

    query = query.offset(skip).limit(limit)
    channels = session.exec(query).all()

    return channels


@router.get("/channels/{channel_id}", response_model=DistributionChannelSchema)
async def get_distribution_channel(
    channel_id: int,
    session: Session = Depends(get_session)
):
    """
    Get specific distribution channel by ID.

    Args:
        channel_id: Channel ID
        session: Database session

    Returns:
        Distribution channel details

    Raises:
        HTTPException: If channel not found
    """
    channel = session.get(DistributionChannel, channel_id)

    if not channel:
        raise HTTPException(status_code=404, detail="Distribution channel not found")

    return channel


@router.put("/channels/{channel_id}", response_model=DistributionChannelSchema)
async def update_distribution_channel(
    channel_id: int,
    channel_update: DistributionChannelUpdate,
    session: Session = Depends(get_session)
):
    """
    Update a distribution channel.

    Args:
        channel_id: Channel ID
        channel_update: Fields to update
        session: Database session

    Returns:
        Updated distribution channel

    Raises:
        HTTPException: If channel not found
    """
    channel = session.get(DistributionChannel, channel_id)

    if not channel:
        raise HTTPException(status_code=404, detail="Distribution channel not found")

    # Update fields if provided
    update_data = channel_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(channel, field, value)

    session.add(channel)
    session.commit()
    session.refresh(channel)

    return channel


@router.delete("/channels/{channel_id}", status_code=204)
async def delete_distribution_channel(
    channel_id: int,
    session: Session = Depends(get_session)
):
    """
    Delete a distribution channel.

    Args:
        channel_id: Channel ID
        session: Database session

    Raises:
        HTTPException: If channel not found
    """
    channel = session.get(DistributionChannel, channel_id)

    if not channel:
        raise HTTPException(status_code=404, detail="Distribution channel not found")

    session.delete(channel)
    session.commit()

    return None


@router.post("/send/{content_id}", response_model=DistributionResponse)
async def distribute_content(
    content_id: int,
    channel_ids: Optional[List[int]] = Query(None, description="Specific channel IDs to use (null = all active)"),
    session: Session = Depends(get_session)
):
    """
    Trigger distribution for generated content.

    NOTE: This is a placeholder implementation. Actual distribution logic
    (sending emails, publishing to web, etc.) will be implemented in Phase 3.

    For now, this endpoint:
    - Validates content exists
    - Finds applicable distribution channels
    - Creates distribution_log entries with status 'pending'
    - Returns list of queued distribution jobs

    Args:
        content_id: Generated content ID
        channel_ids: Optional list of specific channel IDs (defaults to all active)
        session: Database session

    Returns:
        Distribution response with job details

    Raises:
        HTTPException: If content not found or no channels configured
    """
    # Verify content exists
    content = session.get(GeneratedContent, content_id)
    if not content:
        raise HTTPException(
            status_code=404,
            detail=f"Generated content with ID {content_id} not found"
        )

    # Find distribution channels
    if channel_ids:
        # Use specific channels
        channels_query = select(DistributionChannel).where(
            DistributionChannel.id.in_(channel_ids),
            DistributionChannel.template_id == content.template_id,
            DistributionChannel.is_active == True
        )
    else:
        # Use all active channels for this template
        channels_query = select(DistributionChannel).where(
            DistributionChannel.template_id == content.template_id,
            DistributionChannel.is_active == True
        )

    channels = session.exec(channels_query).all()

    if not channels:
        raise HTTPException(
            status_code=404,
            detail="No active distribution channels found for this template"
        )

    # Create distribution log entries (placeholder for actual distribution)
    distribution_jobs = []
    for channel in channels:
        # Create log entry
        log_entry = DistributionLog(
            content_id=content_id,
            channel_id=channel.id,
            status="pending",
            retry_count=0,
        )
        session.add(log_entry)

        # Update channel last_used_at
        channel.last_used_at = datetime.utcnow()
        session.add(channel)

        # Build job info
        job_info = {
            "channel_id": channel.id,
            "channel_name": channel.channel_name,
            "channel_type": channel.channel_type,
            "status": "pending",
            "message": "Queued for distribution (actual delivery not yet implemented)"
        }
        distribution_jobs.append(job_info)

    session.commit()

    return DistributionResponse(
        success=True,
        distribution_jobs=distribution_jobs,
        message=f"Content queued for distribution to {len(channels)} channel(s). Actual delivery will be implemented in Phase 3."
    )


@router.get("/logs/", response_model=List[DistributionLogSchema])
async def list_distribution_logs(
    content_id: Optional[int] = Query(None, description="Filter by content ID"),
    channel_id: Optional[int] = Query(None, description="Filter by channel ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    session: Session = Depends(get_session)
):
    """
    Get distribution logs.

    Args:
        content_id: Filter by content ID (optional)
        channel_id: Filter by channel ID (optional)
        status: Filter by status (optional)
        skip: Number of records to skip
        limit: Maximum records to return
        session: Database session

    Returns:
        List of distribution logs
    """
    query = select(DistributionLog).order_by(DistributionLog.created_at.desc())

    if content_id is not None:
        query = query.where(DistributionLog.content_id == content_id)

    if channel_id is not None:
        query = query.where(DistributionLog.channel_id == channel_id)

    if status:
        query = query.where(DistributionLog.status == status)

    query = query.offset(skip).limit(limit)
    logs = session.exec(query).all()

    return logs


@router.get("/logs/{log_id}", response_model=DistributionLogSchema)
async def get_distribution_log(
    log_id: int,
    session: Session = Depends(get_session)
):
    """
    Get specific distribution log by ID.

    Args:
        log_id: Log ID
        session: Database session

    Returns:
        Distribution log details

    Raises:
        HTTPException: If log not found
    """
    log = session.get(DistributionLog, log_id)

    if not log:
        raise HTTPException(status_code=404, detail="Distribution log not found")

    return log
