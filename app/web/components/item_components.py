"""Item management HTMX components."""

from fastapi import APIRouter, Depends, Query
from fastapi.responses import HTMLResponse
from sqlmodel import Session, text
from typing import Optional
from datetime import datetime, timedelta
from app.core.logging_config import get_logger

from app.database import get_session
from app.repositories.analysis import AnalysisRepo
from .base_component import BaseComponent

router = APIRouter(tags=["htmx-items"])
logger = get_logger(__name__)


class ItemComponent(BaseComponent):
    """Component for item-related HTMX endpoints."""

    @staticmethod
    def generate_geopolitical_display(sentiment_json):
        """Generate HTML for geopolitical analysis display"""
        if not sentiment_json:
            return ''

        geo = sentiment_json.get('geopolitical')
        if not geo:
            return ''

        # Check if has meaningful geopolitical data
        stability = geo.get('stability_score', 0.0)
        security = geo.get('security_relevance', 0.0)
        escalation = geo.get('escalation_potential', 0.0)
        affected = geo.get('impact_affected', [])
        beneficiaries = geo.get('impact_beneficiaries', [])
        conflict_type = geo.get('conflict_type', '')

        # Only show if has meaningful data
        if abs(stability) < 0.1 and security < 0.1 and not affected:
            return ''

        # Stability badge
        stability_color = 'danger' if stability < -0.5 else 'warning' if stability < 0 else 'success'
        stability_icon = '🔴' if stability < -0.5 else '🟡' if stability < 0 else '🟢'

        # Security badge
        security_color = 'danger' if security > 0.7 else 'warning' if security > 0.4 else 'secondary'
        security_icon = '⚠️' if security > 0.7 else '⚡' if security > 0.4 else '🛡️'

        # Escalation badge
        escalation_color = 'danger' if escalation > 0.6 else 'warning' if escalation > 0.3 else 'secondary'

        affected_str = ', '.join(affected[:3]) if affected else '-'
        beneficiaries_str = ', '.join(beneficiaries[:3]) if beneficiaries else '-'

        return f"""
        <div class="geopolitical-analysis p-2 border rounded bg-light">
            <div class="mb-1"><small class="text-muted fw-bold">🌍 Geopolitical</small></div>
            <div class="d-flex flex-column gap-1">
                <span class="badge bg-{stability_color} text-start">
                    {stability_icon} Stability: {stability:.1f}
                </span>
                <span class="badge bg-{security_color} text-start">
                    {security_icon} Security: {security:.1f}
                </span>
                <span class="badge bg-{escalation_color} text-start">
                    📈 Escalation: {escalation:.1f}
                </span>
                {f'<small class="text-muted">Affected: {affected_str}</small>' if affected else ''}
                {f'<small class="text-muted">Benefits: {beneficiaries_str}</small>' if beneficiaries else ''}
                {f'<small class="text-muted">Type: {conflict_type}</small>' if conflict_type else ''}
            </div>
        </div>
        """

    @staticmethod
    def generate_sentiment_display(analysis):
        """Generate HTML for sentiment analysis display - always expanded"""
        if not analysis or not analysis.get('sentiment_json'):
            return '<div class="sentiment-analysis mb-2"><span class="badge bg-secondary">No Analysis</span></div>'

        sentiment_json = analysis.get('sentiment_json', {})
        impact_json = analysis.get('impact_json', {})
        model = analysis.get('model_tag', 'unknown')

        # Extract key values
        overall = sentiment_json.get('overall', {})
        market = sentiment_json.get('market', {})
        label = overall.get('label', 'neutral')
        score = overall.get('score', 0.0)
        confidence = overall.get('confidence', 0.0)
        urgency = sentiment_json.get('urgency', 0.0)
        impact_overall = impact_json.get('overall', 0.0)
        impact_volatility = impact_json.get('volatility', 0.0)
        themes = sentiment_json.get('themes', [])

        # Sentiment icon and color
        if label == 'positive':
            icon = '🟢'
            color = 'success'
        elif label == 'negative':
            icon = '🔴'
            color = 'danger'
        else:
            icon = '⚪'
            color = 'secondary'

        # Market display
        market_display = f"📉 Bearish ({market.get('bearish', 0):.1f})" if market.get('bearish', 0) > 0.6 else f"📈 Bullish ({market.get('bullish', 0):.1f})" if market.get('bullish', 0) > 0.6 else "➡️ Neutral"
        time_horizon = market.get('time_horizon', 'medium').title()
        themes_display = ' • '.join([f"🏷️ {theme}" for theme in themes[:4]])  # Show max 4 themes

        return f"""
        <div class="sentiment-analysis mb-2">
            <div class="card border-light bg-light">
                <div class="card-header bg-transparent border-bottom-0 py-2">
                    <h6 class="mb-0 text-muted">📊 Sentiment ({model})</h6>
                </div>
                <div class="card-body py-2">
                    <div class="mb-2">
                        <span class="badge bg-{color}">{icon} {label.title()} ({score:.1f})</span>
                        <small class="text-muted">• {int(confidence*100)}% confident</small>
                    </div>
                    <div class="mb-2">
                        <strong>Market:</strong> {market_display} • {time_horizon}-term
                    </div>
                    <div class="mb-2">
                        <strong>Impact:</strong> ⚡ {impact_overall:.1f} • Volatility: 📈 {impact_volatility:.1f}
                    </div>
                    <div class="mb-2">
                        <strong>Urgency:</strong> ⏰ {urgency:.1f}
                    </div>
                    {f'<div class="mt-2"><strong>Themes:</strong> {themes_display}</div>' if themes else ''}
                </div>
            </div>
        </div>
        """

    @staticmethod
    def build_item_card(item_data: dict) -> str:
        """Build HTML for a single item card with 3-column layout."""
        published_date = ItemComponent.format_date(item_data.get('published')) if item_data.get('published') else ItemComponent.format_date(item_data.get('created_at'))
        description = ItemComponent.truncate_text(item_data.get('description', ''), 200)

        # Clean and escape content
        clean_title = ItemComponent.clean_html_attr(item_data.get('title', 'Untitled'))
        clean_description = ItemComponent.clean_html_attr(description)
        feed_name = item_data.get('feed_title', item_data.get('feed_url', 'Unknown Feed')[:30] + "...")

        author_info = f'<span><i class="bi bi-person me-1"></i>{item_data.get("author")}</span>' if item_data.get('author') else ''

        # Get analysis data for sentiment and geopolitical display
        analysis = AnalysisRepo.get_by_item_id(item_data.get('id'))
        analysis_display = ItemComponent.generate_sentiment_display(analysis)

        # Get geopolitical display
        sentiment_json = analysis.get('sentiment_json', {}) if analysis else {}
        geopolitical_display = ItemComponent.generate_geopolitical_display(sentiment_json)

        return f'''
        <div class="card mb-3 shadow-sm">
            <div class="card-body">
                <div class="row">
                    <!-- Left Column: Title and Metadata -->
                    <div class="col-md-6">
                        <h5 class="card-title mb-2">
                            <a href="{item_data.get('link', '#')}" target="_blank" class="text-decoration-none text-primary">
                                {clean_title}
                            </a>
                        </h5>
                        <div class="d-flex flex-wrap gap-3 text-muted small mb-2">
                            <span><i class="bi bi-calendar me-1"></i>{published_date}</span>
                            <span><i class="bi bi-rss me-1"></i>{feed_name}</span>
                            {author_info}
                        </div>
                        {f'<p class="card-text text-body-secondary small">{clean_description}</p>' if clean_description else ''}
                    </div>

                    <!-- Middle Column: Classic Sentiment -->
                    <div class="col-md-3">
                        {analysis_display}
                    </div>

                    <!-- Right Column: Geopolitical Sentiment -->
                    <div class="col-md-3">
                        {geopolitical_display if geopolitical_display else '<div class="text-center text-muted small mt-4">No geopolitical data</div>'}
                    </div>
                </div>
            </div>
        </div>
        '''


@router.get("/items-list", response_class=HTMLResponse)
def get_items_list(
    session: Session = Depends(get_session),
    category_id: Optional[int] = Query(None),
    feed_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    since_hours: Optional[int] = Query(None),
    skip: int = 0,
    limit: int = 20
):
    """Get filtered HTML list of items."""
    try:
        # Use raw SQL to avoid SQLModel issues
        where_clauses = []
        params = {}

        if category_id and category_id > 0:
            where_clauses.append("""
                i.feed_id IN (
                    SELECT feed_id FROM feed_categories WHERE category_id = :category_id
                )
            """)
            params['category_id'] = category_id

        if feed_id and feed_id > 0:
            where_clauses.append("i.feed_id = :feed_id")
            params['feed_id'] = feed_id

        if since_hours and since_hours > 0:
            since_time = datetime.utcnow() - timedelta(hours=since_hours)
            where_clauses.append("i.created_at >= :since_time")
            params['since_time'] = since_time

        if search:
            where_clauses.append("(i.title ILIKE :search OR i.description ILIKE :search)")
            params['search'] = f'%{search}%'

        where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

        sql = f"""
            SELECT
                i.id, i.title, i.link, i.description, i.author, i.published, i.created_at,
                f.id as feed_id, f.title as feed_title, f.url as feed_url
            FROM items i
            JOIN feeds f ON i.feed_id = f.id
            {where_sql}
            ORDER BY COALESCE(i.published, i.created_at) DESC
            LIMIT :limit OFFSET :skip
        """

        params['limit'] = limit
        params['skip'] = skip

        # Execute raw SQL
        result = session.execute(text(sql), params)
        items = result.fetchall()

        # Build HTML
        html = ""
        for row in items:
            item_data = {
                'id': row[0],
                'title': row[1],
                'link': row[2],
                'description': row[3],
                'author': row[4],
                'published': row[5],
                'created_at': row[6],
                'feed_id': row[7],
                'feed_title': row[8],
                'feed_url': row[9]
            }
            html += ItemComponent.build_item_card(item_data)

        if not html:
            html = BaseComponent.alert_box('No articles found.', 'info')

        return html

    except Exception as e:
        logger.error(f"Error in items-list: {e}")
        return BaseComponent.alert_box(f'Error loading articles: {str(e)}', 'danger')