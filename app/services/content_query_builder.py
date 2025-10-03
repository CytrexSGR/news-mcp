"""
Content Query Builder Service.

Builds SQL queries from template selection criteria and estimates costs.
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from sqlmodel import Session, select, or_
from decimal import Decimal

from app.models.core import Item
from app.models.analysis import ItemAnalysis
from app.models.content_distribution import ContentTemplate


def build_article_query(
    criteria: Dict[str, Any],
    session: Session
) -> List[Item]:
    """
    Build and execute article query from template selection criteria.

    Args:
        criteria: Selection criteria from template
        session: Database session

    Returns:
        List of matching Item objects

    Criteria structure:
    {
        "keywords": ["security", "breach"],
        "exclude_keywords": ["opinion"],
        "timeframe_hours": 24,
        "min_impact_score": 0.7,
        "min_sentiment_score": -1.0,
        "feed_ids": [1, 5, 12],
        "category_names": ["Technology"],
        "source_names": ["TechCrunch"],
        "max_articles": 50
    }
    """
    # Start with base query joining Item and ItemAnalysis
    query = select(Item).join(ItemAnalysis, isouter=True)

    # Time filter
    if criteria.get("timeframe_hours"):
        cutoff = datetime.utcnow() - timedelta(hours=criteria["timeframe_hours"])
        query = query.where(Item.published >= cutoff)

    # Keywords (OR condition - at least one must match)
    if criteria.get("keywords"):
        keyword_filters = [
            Item.title.ilike(f"%{kw}%") for kw in criteria["keywords"]
        ]
        query = query.where(or_(*keyword_filters))

    # Exclude keywords (AND NOT condition - none must match)
    if criteria.get("exclude_keywords"):
        for kw in criteria["exclude_keywords"]:
            query = query.where(~Item.title.ilike(f"%{kw}%"))

    # Impact score filter (from JSON)
    if criteria.get("min_impact_score") is not None:
        from sqlalchemy import cast, Float
        query = query.where(
            cast(ItemAnalysis.impact_json['overall'], Float) >= criteria["min_impact_score"]
        )

    # Sentiment score filter (from JSON)
    if criteria.get("min_sentiment_score") is not None:
        from sqlalchemy import cast, Float
        query = query.where(
            cast(ItemAnalysis.sentiment_json['overall']['score'], Float) >= criteria["min_sentiment_score"]
        )

    # Feed filter
    if criteria.get("feed_ids"):
        query = query.where(Item.feed_id.in_(criteria["feed_ids"]))

    # Category filter (would need join to Feed and Category)
    # TODO: Implement category filtering if needed

    # Source filter (would need join to Feed and Source)
    # TODO: Implement source filtering if needed

    # Order by impact score (from JSON, descending) and recency
    from sqlalchemy import cast, Float, desc, nullslast
    query = query.order_by(
        nullslast(desc(cast(ItemAnalysis.impact_json['overall'], Float))),
        Item.published.desc()
    )

    # Limit
    max_articles = criteria.get("max_articles", 50)
    query = query.limit(max_articles)

    # Execute and return
    articles = session.exec(query).all()
    return articles


def estimate_generation_cost(
    template: ContentTemplate,
    article_count: int
) -> float:
    """
    Estimate OpenAI API cost for content generation.

    Based on:
    - Input tokens (articles + prompt template)
    - Output tokens (expected content length from structure)
    - Model pricing

    Args:
        template: Content template
        article_count: Number of articles to process

    Returns:
        Estimated cost in USD
    """
    # Pricing (as of 2025-10) - Update as needed
    PRICING = {
        "gpt-4o": {
            "input": 0.0025,   # per 1K tokens
            "output": 0.01     # per 1K tokens
        },
        "gpt-4o-mini": {
            "input": 0.00015,  # per 1K tokens
            "output": 0.0006   # per 1K tokens
        },
        "gpt-4-turbo": {
            "input": 0.01,     # per 1K tokens
            "output": 0.03     # per 1K tokens
        }
    }

    model = template.llm_model
    if model not in PRICING:
        model = "gpt-4o-mini"  # Default fallback

    # Estimate input tokens
    # Average article: ~500 tokens (title + summary + metadata)
    input_tokens = (article_count * 500)

    # Prompt template: ~1000 tokens
    input_tokens += 1000

    # Estimate output tokens from content structure
    output_tokens = 0
    for section in template.content_structure.get("sections", []):
        max_words = section.get("max_words") or section.get("max_items", 200)  # Fallback to max_items or 200
        # Words to tokens ratio: ~1.3
        section_tokens = int(max_words * 1.3)
        output_tokens += section_tokens

    # Minimum output tokens if no sections
    if output_tokens == 0:
        output_tokens = 2000  # Default 2000 tokens (~1500 words)

    # Calculate cost
    cost_per_1k_input = PRICING[model]["input"]
    cost_per_1k_output = PRICING[model]["output"]

    total_cost = (
        (input_tokens / 1000) * cost_per_1k_input +
        (output_tokens / 1000) * cost_per_1k_output
    )

    return round(total_cost, 6)


def validate_selection_criteria(criteria: Dict[str, Any]) -> List[str]:
    """
    Validate selection criteria and return list of errors.

    Args:
        criteria: Selection criteria dict

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    # Check required fields
    if not criteria:
        errors.append("Selection criteria cannot be empty")
        return errors

    # Validate timeframe
    if "timeframe_hours" in criteria:
        if not isinstance(criteria["timeframe_hours"], int) or criteria["timeframe_hours"] < 1:
            errors.append("timeframe_hours must be a positive integer")

    # Validate scores
    if "min_impact_score" in criteria:
        score = criteria["min_impact_score"]
        if not isinstance(score, (int, float)) or score < 0 or score > 1:
            errors.append("min_impact_score must be between 0.0 and 1.0")

    if "min_sentiment_score" in criteria:
        score = criteria["min_sentiment_score"]
        if not isinstance(score, (int, float)) or score < -1 or score > 1:
            errors.append("min_sentiment_score must be between -1.0 and 1.0")

    # Validate lists
    if "keywords" in criteria and not isinstance(criteria["keywords"], list):
        errors.append("keywords must be a list")

    if "exclude_keywords" in criteria and not isinstance(criteria["exclude_keywords"], list):
        errors.append("exclude_keywords must be a list")

    if "feed_ids" in criteria and not isinstance(criteria["feed_ids"], list):
        errors.append("feed_ids must be a list")

    # Validate max_articles
    if "max_articles" in criteria:
        max_articles = criteria["max_articles"]
        if not isinstance(max_articles, int) or max_articles < 1 or max_articles > 500:
            errors.append("max_articles must be between 1 and 500")

    return errors
