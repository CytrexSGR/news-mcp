"""
API endpoints for Generated Content management.

Provides endpoints to view and manage generated content.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

from app.database import get_session
from app.models.content_distribution import GeneratedContent, ContentTemplate
from app.schemas.content_distribution import (
    GeneratedContent as GeneratedContentSchema,
    GeneratedContentSummary,
)

router = APIRouter(prefix="/content", tags=["content"])


@router.get("/", response_model=List[GeneratedContentSummary])
async def list_generated_content(
    template_id: Optional[int] = Query(None, description="Filter by template ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    session: Session = Depends(get_session)
):
    """
    List generated content.

    Args:
        template_id: Filter by template ID (optional)
        status: Filter by status (optional)
        skip: Number of records to skip
        limit: Maximum records to return
        session: Database session

    Returns:
        List of generated content summaries
    """
    query = select(GeneratedContent).order_by(GeneratedContent.generated_at.desc())

    if template_id:
        query = query.where(GeneratedContent.template_id == template_id)

    if status:
        query = query.where(GeneratedContent.status == status)

    query = query.offset(skip).limit(limit)
    content_list = session.exec(query).all()

    # Build summaries with template name
    summaries = []
    for content in content_list:
        template = session.get(ContentTemplate, content.template_id)
        summaries.append(
            GeneratedContentSummary(
                id=content.id,
                template_id=content.template_id,
                template_name=template.name if template else "Unknown",
                title=content.title,
                status=content.status,
                generated_at=content.generated_at,
                articles_count=content.articles_count,
                word_count=content.word_count,
                generation_cost_usd=float(content.generation_cost_usd) if content.generation_cost_usd else None
            )
        )

    return summaries


@router.get("/{content_id}", response_model=GeneratedContentSchema)
async def get_generated_content(
    content_id: int,
    session: Session = Depends(get_session)
):
    """
    Get specific generated content by ID.

    Args:
        content_id: Content ID
        session: Database session

    Returns:
        Generated content details

    Raises:
        HTTPException: If content not found
    """
    content = session.get(GeneratedContent, content_id)

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    return content


@router.get("/latest/{template_id}", response_model=GeneratedContentSchema)
async def get_latest_content(
    template_id: int,
    session: Session = Depends(get_session)
):
    """
    Get most recent generated content for a template.

    Args:
        template_id: Template ID
        session: Database session

    Returns:
        Latest generated content

    Raises:
        HTTPException: If no content found for template
    """
    content = session.exec(
        select(GeneratedContent)
        .where(GeneratedContent.template_id == template_id)
        .order_by(GeneratedContent.generated_at.desc())
    ).first()

    if not content:
        raise HTTPException(
            status_code=404,
            detail=f"No content found for template {template_id}"
        )

    return content


@router.delete("/{content_id}", status_code=204)
async def delete_generated_content(
    content_id: int,
    session: Session = Depends(get_session)
):
    """
    Delete generated content.

    Args:
        content_id: Content ID
        session: Database session

    Raises:
        HTTPException: If content not found
    """
    content = session.get(GeneratedContent, content_id)

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    session.delete(content)
    session.commit()

    return None
