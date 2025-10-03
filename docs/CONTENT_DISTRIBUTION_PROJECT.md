# Content Distribution System - Implementation Project

**Status:** Planning Phase
**Started:** 2025-10-02
**Target MVP:** 2025-10-16 (2 weeks)
**Current Phase:** Phase 0 - Setup & Planning

---

## 🎯 Project Vision

Transform News MCP from internal news aggregator into a **Content Distribution Platform** that:
- Creates structured, audience-specific briefings from raw news data
- Automatically generates content using LLM-powered templates
- Distributes via multiple channels (Email, Web, RSS, API)
- Manages the complete content lifecycle through web interface

---

## 📊 Project Status Dashboard

### Overall Progress: 0% (0/50 tasks completed)

**Phase Status:**
- ✅ Phase 0: Setup & Planning (0/5) - IN PROGRESS
- ⏳ Phase 1: Foundation (0/10) - NOT STARTED
- ⏳ Phase 2: Content Generation (0/12) - NOT STARTED
- ⏳ Phase 3: Distribution (0/10) - NOT STARTED
- ⏳ Phase 4: Automation (0/8) - NOT STARTED
- ⏳ Phase 5: Polish (0/5) - NOT STARTED

---

## 🏗️ Architecture Overview

### System Layers

```
┌─────────────────────────────────────────────────┐
│  Distribution Layer (NEW)                       │
│  Email | Web | RSS | API                        │
└─────────────────────────────────────────────────┘
           ↑
┌─────────────────────────────────────────────────┐
│  Content Generation Layer (NEW)                 │
│  Templates → LLM Processing → Structured Output │
└─────────────────────────────────────────────────┘
           ↑
┌─────────────────────────────────────────────────┐
│  Data Foundation (EXISTING) ✅                   │
│  41 Feeds → 20k Articles → AI Analysis          │
└─────────────────────────────────────────────────┘
```

### New Components

1. **Template System** - Define content structure and selection criteria
2. **Content Generator Worker** - LLM-powered content creation
3. **Distribution Engine** - Multi-channel delivery
4. **Management UI** - Template & content lifecycle management

---

## 📋 Implementation Roadmap

### Phase 0: Setup & Planning (Current Phase)
**Duration:** Day 1
**Goal:** Project structure, documentation, initial planning

- [ ] Create project documentation (`CONTENT_DISTRIBUTION_PROJECT.md`)
- [ ] Create development tracker (`DEVELOPMENT_LOG.md`)
- [ ] Review resource requirements
- [ ] Set up development branch strategy
- [ ] Stakeholder alignment on MVP scope

**Deliverables:**
- Project plan document ✅ (this file)
- Development log template
- Resource assessment

---

### Phase 1: Foundation (Database & API)
**Duration:** Days 2-4 (3 days)
**Goal:** Database schema, basic CRUD API, template data model

#### Database Tasks (4 tasks)
- [ ] Design `content_templates` table schema
- [ ] Design `generated_content` table schema
- [ ] Design `distribution_channels` table schema
- [ ] Design `distribution_log` table schema
- [ ] Create Alembic migration for all tables
- [ ] Run migration and verify schema

#### API Endpoints (6 tasks)
- [ ] `POST /api/v2/templates/` - Create template
- [ ] `GET /api/v2/templates/` - List templates
- [ ] `GET /api/v2/templates/{id}` - Get template details
- [ ] `PUT /api/v2/templates/{id}` - Update template
- [ ] `DELETE /api/v2/templates/{id}` - Delete template
- [ ] `POST /api/v2/templates/{id}/test` - Test template (preview)

#### Models & Schemas (2 tasks)
- [ ] Create Pydantic models for templates
- [ ] Create database ORM models (SQLAlchemy)

**Deliverables:**
- 4 database tables operational
- 6 REST API endpoints tested
- API documentation updated

**Success Criteria:**
- Can create template via API
- Can query articles matching template criteria
- Template data persists correctly

---

### Phase 2: Content Generation
**Duration:** Days 5-9 (5 days)
**Goal:** LLM-powered content generation, worker implementation

#### Content Generator Worker (5 tasks)
- [ ] Create `content_generator_worker.py` (copy analysis_worker pattern)
- [ ] Implement article query builder (template criteria → SQL)
- [ ] Implement context preparation (articles → LLM input format)
- [ ] Implement LLM prompt processing (template + articles → structured output)
- [ ] Implement content storage (save to `generated_content` table)

#### Generation Queue (3 tasks)
- [ ] Create `pending_content_generation` table
- [ ] Implement queue management service
- [ ] Add manual generation trigger endpoint

#### LLM Integration (4 tasks)
- [ ] Design base prompt template structure
- [ ] Implement JSON schema validation for LLM output
- [ ] Add retry logic for malformed outputs
- [ ] Add cost tracking per generation

**API Endpoints:**
- [ ] `POST /api/v2/content/generate/{template_id}` - Trigger generation
- [ ] `GET /api/v2/content/` - List generated content
- [ ] `GET /api/v2/content/{id}` - Get content details
- [ ] `GET /api/v2/content/latest/{template_id}` - Get latest for template

**Deliverables:**
- Content generation worker operational
- Manual content generation works end-to-end
- Generated content stored correctly

**Success Criteria:**
- Can trigger content generation for template
- LLM produces structured output
- Output validates against schema
- Content stored in database

---

### Phase 3: Distribution
**Duration:** Days 10-13 (4 days)
**Goal:** Email, Web, RSS distribution channels

#### Email Channel (4 tasks)
- [ ] Implement SMTP email sender (`email_distribution.py`)
- [ ] Create HTML email template (Jinja2)
- [ ] Add recipient list management
- [ ] Add email delivery logging

#### Web Publication (3 tasks)
- [ ] Create `/briefings/{template}/{date}` endpoint
- [ ] Create briefing display template (HTML)
- [ ] Add access control (public/private toggle)

#### RSS Feed (3 tasks)
- [ ] Implement RSS feed generator (`feedgen` library)
- [ ] Create `/feeds/generated/{template}.xml` endpoint
- [ ] Add automatic feed updates on new content

**API Endpoints:**
- [ ] `POST /api/v2/distribution/channels/` - Add distribution channel
- [ ] `GET /api/v2/distribution/channels/` - List channels
- [ ] `POST /api/v2/distribution/send/{content_id}` - Trigger distribution
- [ ] `GET /api/v2/distribution/logs/` - Get delivery logs

**Deliverables:**
- Email distribution functional
- Web publication accessible
- RSS feed generated

**Success Criteria:**
- Can send generated content via email
- Can view briefing on web URL
- RSS feed validates and updates

---

### Phase 4: Automation
**Duration:** Days 14-16 (3 days)
**Goal:** Scheduled generation, distribution worker, monitoring

#### Scheduling (3 tasks)
- [ ] Implement cron-based template scheduler
- [ ] Add on-demand generation triggers
- [ ] Add real-time triggers (on new matching articles)

#### Distribution Worker (3 tasks)
- [ ] Create `distribution_worker.py`
- [ ] Implement automatic distribution on content generation
- [ ] Add retry logic for failed deliveries

#### Monitoring (2 tasks)
- [ ] Add generation job tracking
- [ ] Add distribution metrics dashboard

**Deliverables:**
- Scheduled content generation works
- Automatic distribution on schedule
- Job monitoring in place

**Success Criteria:**
- Template generates content at scheduled time
- Content automatically distributed via configured channels
- Failed jobs logged and retryable

---

### Phase 5: UI & Polish
**Duration:** Days 17-20 (4 days)
**Goal:** Management UI, documentation, testing

#### Admin UI (5 tasks)
- [ ] Create `/admin/templates` page (list + CRUD)
- [ ] Create template creation wizard
- [ ] Create `/admin/content` page (content library)
- [ ] Create `/admin/distribution` page (channel management)
- [ ] Create `/admin/generation-jobs` page (job monitoring)

#### Documentation & Testing (3 tasks)
- [ ] Update API documentation (OpenAPI)
- [ ] Write user guide for template creation
- [ ] Create end-to-end integration tests

**Deliverables:**
- Complete admin UI for all features
- User documentation
- Test coverage

**Success Criteria:**
- Can create template entirely through UI
- Can monitor content generation and distribution
- Documentation is complete

---

## 🎯 MVP Scope (3-Week Target)

**Minimum Viable Product includes:**

✅ **Core Features:**
- Template CRUD (via API and UI)
- Content generation (LLM-powered)
- Email distribution
- Web publication
- Manual generation triggers

✅ **1 Complete Use Case:**
- "IT Manager Security Brief" template
- Daily generation at 8am
- Email to distribution list
- Published to `/briefings/security/latest`

❌ **Out of MVP Scope (Post-launch):**
- RSS feed generation → Phase 3 Post-MVP
- API webhooks → Phase 4
- Advanced scheduling (real-time) → Phase 4
- Template wizard → Phase 5
- Analytics/metrics → Phase 5
- A/B testing → Future
- Multi-user/auth → Future

---

## 📦 Database Schema Design

### Table: `content_templates`

```sql
CREATE TABLE content_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL UNIQUE,
    description TEXT,
    target_audience VARCHAR(100),

    -- Selection Criteria (JSON)
    selection_criteria JSONB NOT NULL,
    -- Example: {
    --   "keywords": ["security", "breach"],
    --   "timeframe_hours": 12,
    --   "min_impact_score": 0.7,
    --   "feed_ids": [1, 5, 12],
    --   "categories": ["Technology"],
    --   "max_articles": 50
    -- }

    -- Content Structure (JSON)
    content_structure JSONB NOT NULL,
    -- Example: {
    --   "sections": [
    --     {"name": "executive_summary", "max_words": 150},
    --     {"name": "critical_alerts", "format": "list"},
    --     {"name": "recommendations", "max_items": 5}
    --   ],
    --   "output_format": "markdown"
    -- }

    -- LLM Configuration
    llm_prompt_template TEXT NOT NULL,
    llm_model VARCHAR(50) DEFAULT 'gpt-4o-mini',
    llm_temperature DECIMAL(3,2) DEFAULT 0.7,

    -- Scheduling
    generation_schedule VARCHAR(100),
    -- Examples: "0 8 * * *" (cron), "on_demand", "realtime"

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    -- Metadata
    version INTEGER DEFAULT 1,
    tags JSONB,

    CONSTRAINT valid_schedule CHECK (
        generation_schedule IS NULL OR
        generation_schedule ~ '^([0-9*,/-]+ ){4}[0-9*,/-]+$|^(on_demand|realtime)$'
    )
);

CREATE INDEX idx_templates_active ON content_templates(is_active);
CREATE INDEX idx_templates_schedule ON content_templates(generation_schedule);
```

### Table: `generated_content`

```sql
CREATE TABLE generated_content (
    id SERIAL PRIMARY KEY,
    template_id INTEGER NOT NULL REFERENCES content_templates(id) ON DELETE CASCADE,

    -- Generated Content
    title VARCHAR(500),
    content_html TEXT,
    content_markdown TEXT,
    content_json JSONB,

    -- Metadata
    generated_at TIMESTAMP DEFAULT NOW(),
    generation_job_id VARCHAR(100),

    -- Source Tracking
    source_article_ids INTEGER[] NOT NULL,
    -- Array of item IDs used as input
    articles_count INTEGER NOT NULL,

    -- Quality Metrics
    word_count INTEGER,
    generation_cost_usd DECIMAL(10, 6),
    generation_time_seconds INTEGER,
    llm_model_used VARCHAR(50),

    -- Status
    status VARCHAR(20) DEFAULT 'generated',
    -- Values: generated, published, archived, failed
    published_at TIMESTAMP,
    error_message TEXT,

    CONSTRAINT valid_status CHECK (
        status IN ('generated', 'published', 'archived', 'failed')
    )
);

CREATE INDEX idx_content_template ON generated_content(template_id);
CREATE INDEX idx_content_generated_at ON generated_content(generated_at DESC);
CREATE INDEX idx_content_status ON generated_content(status);
```

### Table: `distribution_channels`

```sql
CREATE TABLE distribution_channels (
    id SERIAL PRIMARY KEY,
    template_id INTEGER NOT NULL REFERENCES content_templates(id) ON DELETE CASCADE,

    -- Channel Configuration
    channel_type VARCHAR(20) NOT NULL,
    -- Values: email, web, rss, api
    channel_name VARCHAR(200) NOT NULL,
    channel_config JSONB NOT NULL,
    -- Email example: {
    --   "recipients": ["team@example.com"],
    --   "subject_template": "Security Brief - {date}",
    --   "from_address": "briefings@news-mcp.com"
    -- }
    -- Web example: {
    --   "publish_url": "/briefings/security/{date}",
    --   "access": "public"
    -- }

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_used_at TIMESTAMP,

    CONSTRAINT valid_channel_type CHECK (
        channel_type IN ('email', 'web', 'rss', 'api')
    ),
    CONSTRAINT unique_channel_per_template UNIQUE (template_id, channel_type, channel_name)
);

CREATE INDEX idx_channels_template ON distribution_channels(template_id);
CREATE INDEX idx_channels_type ON distribution_channels(channel_type);
CREATE INDEX idx_channels_active ON distribution_channels(is_active);
```

### Table: `distribution_log`

```sql
CREATE TABLE distribution_log (
    id SERIAL PRIMARY KEY,
    content_id INTEGER NOT NULL REFERENCES generated_content(id) ON DELETE CASCADE,
    channel_id INTEGER NOT NULL REFERENCES distribution_channels(id) ON DELETE CASCADE,

    -- Distribution Status
    status VARCHAR(20) DEFAULT 'pending',
    -- Values: pending, sent, failed, retry
    sent_at TIMESTAMP,

    -- Delivery Details
    recipient_count INTEGER,
    recipients_list JSONB,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,

    -- Tracking (optional)
    open_count INTEGER DEFAULT 0,
    click_count INTEGER DEFAULT 0,
    tracking_enabled BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT valid_status CHECK (
        status IN ('pending', 'sent', 'failed', 'retry')
    )
);

CREATE INDEX idx_distlog_content ON distribution_log(content_id);
CREATE INDEX idx_distlog_channel ON distribution_log(channel_id);
CREATE INDEX idx_distlog_status ON distribution_log(status);
CREATE INDEX idx_distlog_sent_at ON distribution_log(sent_at DESC);
```

### Table: `pending_content_generation` (Queue)

```sql
CREATE TABLE pending_content_generation (
    id SERIAL PRIMARY KEY,
    template_id INTEGER NOT NULL REFERENCES content_templates(id) ON DELETE CASCADE,

    -- Queue Status
    status VARCHAR(20) DEFAULT 'pending',
    -- Values: pending, processing, completed, failed
    created_at TIMESTAMP DEFAULT NOW(),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,

    -- Processing Info
    worker_id VARCHAR(100),
    generated_content_id INTEGER REFERENCES generated_content(id),
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,

    -- Metadata
    triggered_by VARCHAR(50) DEFAULT 'manual',
    -- Values: manual, scheduled, realtime

    CONSTRAINT valid_status CHECK (
        status IN ('pending', 'processing', 'completed', 'failed')
    )
);

CREATE INDEX idx_pending_generation_status ON pending_content_generation(status);
CREATE INDEX idx_pending_generation_created ON pending_content_generation(created_at);
CREATE INDEX idx_pending_generation_template ON pending_content_generation(template_id);
```

---

## 🔧 Technical Implementation Details

### Content Generator Worker Architecture

**File:** `app/workers/content_generator_worker.py`

**Pattern:** Copy from `analysis_worker.py` with modifications

```python
class ContentGeneratorWorker:
    """
    Worker that processes pending content generation jobs.

    Workflow:
    1. Poll pending_content_generation table
    2. For each pending job:
       a. Load template configuration
       b. Query articles matching selection criteria
       c. Prepare context for LLM
       d. Call OpenAI API with template prompt
       e. Validate and parse LLM output
       f. Store in generated_content table
       g. Trigger distribution (if auto-distribute enabled)
    """

    async def process_pending_queue(self):
        """Main processing loop"""
        pass

    async def generate_content(self, template_id: int) -> GeneratedContent:
        """Generate content for specific template"""

        # 1. Load template
        template = await self.get_template(template_id)

        # 2. Query articles
        articles = await self.query_articles(template.selection_criteria)

        # 3. Prepare LLM context
        context = await self.prepare_context(articles, template)

        # 4. Call LLM
        llm_output = await self.call_llm(
            prompt=template.llm_prompt_template.format(**context),
            model=template.llm_model
        )

        # 5. Validate output
        validated = await self.validate_output(llm_output, template.content_structure)

        # 6. Store content
        content = await self.store_content(
            template_id=template_id,
            output=validated,
            source_articles=articles
        )

        return content
```

### Article Query Builder

**Purpose:** Convert template selection criteria → SQL query

```python
def build_article_query(criteria: dict) -> Query:
    """
    Build SQLAlchemy query from template selection criteria.

    Criteria example:
    {
        "keywords": ["security", "breach"],
        "timeframe_hours": 12,
        "min_impact_score": 0.7,
        "feed_ids": [1, 5, 12],
        "categories": ["Technology"],
        "max_articles": 50,
        "exclude_keywords": ["spam"]
    }
    """
    query = db.query(Item).join(ItemAnalysis)

    # Time filter
    if criteria.get("timeframe_hours"):
        cutoff = datetime.now() - timedelta(hours=criteria["timeframe_hours"])
        query = query.filter(Item.published >= cutoff)

    # Keywords (OR condition)
    if criteria.get("keywords"):
        keyword_filters = [
            Item.title.ilike(f"%{kw}%") for kw in criteria["keywords"]
        ]
        query = query.filter(or_(*keyword_filters))

    # Exclude keywords (AND NOT condition)
    if criteria.get("exclude_keywords"):
        for kw in criteria["exclude_keywords"]:
            query = query.filter(~Item.title.ilike(f"%{kw}%"))

    # Impact score
    if criteria.get("min_impact_score"):
        query = query.filter(
            ItemAnalysis.impact_score >= criteria["min_impact_score"]
        )

    # Feed filter
    if criteria.get("feed_ids"):
        query = query.filter(Item.feed_id.in_(criteria["feed_ids"]))

    # Category filter
    if criteria.get("categories"):
        query = query.join(Feed).join(Category).filter(
            Category.name.in_(criteria["categories"])
        )

    # Order by impact/recency
    query = query.order_by(
        ItemAnalysis.impact_score.desc(),
        Item.published.desc()
    )

    # Limit
    max_articles = criteria.get("max_articles", 50)
    query = query.limit(max_articles)

    return query
```

### LLM Prompt Template Structure

```python
# Base template with variables
BASE_PROMPT = """
You are a professional news analyst creating a {target_audience} briefing.

**Context:**
- Time Period: {timeframe}
- Total Articles Analyzed: {article_count}
- Selection Criteria: {criteria_summary}

**Source Articles:**
{articles_list}

**Task:**
Generate a structured briefing with the following sections:
{sections_definition}

**Output Format:**
{output_format_instructions}

**Guidelines:**
- Be concise and professional
- Prioritize by impact/urgency
- Include actionable insights
- Cite sources where relevant

Generate the briefing now:
"""

# Articles list formatting
ARTICLE_FORMAT = """
---
Title: {title}
Source: {feed_name}
Published: {published_at}
Impact Score: {impact_score}/1.0
Sentiment: {sentiment_label} ({sentiment_score})
Summary: {summary}
URL: {link}
---
"""
```

### Email Distribution Implementation

```python
# app/services/email_distribution.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template

class EmailDistributor:
    """Handle email distribution of generated content"""

    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "localhost")
        self.smtp_port = int(os.getenv("SMTP_PORT", 1025))
        self.from_address = os.getenv("EMAIL_FROM", "briefings@news-mcp.com")

    async def send_briefing(
        self,
        content: GeneratedContent,
        channel_config: dict
    ) -> DistributionLog:
        """Send content via email"""

        # Load email template
        template = Template(EMAIL_TEMPLATE_HTML)

        # Render email content
        html_body = template.render(
            title=content.title,
            content=content.content_html,
            generated_at=content.generated_at,
            source_count=content.articles_count
        )

        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = channel_config['subject_template'].format(
            date=content.generated_at.strftime('%Y-%m-%d')
        )
        msg['From'] = self.from_address
        msg['To'] = ', '.join(channel_config['recipients'])

        # Attach HTML content
        msg.attach(MIMEText(html_body, 'html'))

        # Send via SMTP
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.send_message(msg)

            # Log success
            return await self.log_distribution(
                content_id=content.id,
                status='sent',
                recipient_count=len(channel_config['recipients'])
            )

        except Exception as e:
            # Log failure
            return await self.log_distribution(
                content_id=content.id,
                status='failed',
                error_message=str(e)
            )
```

---

## 📝 API Documentation

### Template Management Endpoints

#### POST /api/v2/templates/

Create new content template.

**Request Body:**
```json
{
  "name": "IT Manager Security Brief",
  "description": "Daily security briefing for IT management",
  "target_audience": "IT Managers",
  "selection_criteria": {
    "keywords": ["security", "breach", "vulnerability", "CVE"],
    "timeframe_hours": 24,
    "min_impact_score": 0.6,
    "feed_ids": [1, 5, 8, 12],
    "max_articles": 30
  },
  "content_structure": {
    "sections": [
      {
        "name": "executive_summary",
        "max_words": 150,
        "prompt": "Provide a concise executive summary"
      },
      {
        "name": "critical_alerts",
        "format": "list",
        "prompt": "List all critical security alerts"
      },
      {
        "name": "recommendations",
        "max_items": 5,
        "prompt": "Provide actionable recommendations"
      }
    ],
    "output_format": "markdown"
  },
  "llm_prompt_template": "You are generating a security briefing...",
  "llm_model": "gpt-4o-mini",
  "generation_schedule": "0 8 * * *",
  "is_active": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "IT Manager Security Brief",
    "created_at": "2025-10-02T10:00:00Z",
    ...
  }
}
```

#### GET /api/v2/templates/{id}/test

Test template without saving (dry-run).

**Response:**
```json
{
  "success": true,
  "preview": {
    "matching_articles": 18,
    "estimated_cost": 0.025,
    "sample_articles": [
      {
        "title": "Critical vulnerability in OpenSSL",
        "impact_score": 0.95,
        "published": "2025-10-02T08:30:00Z"
      }
    ],
    "llm_context_size": 4500
  }
}
```

### Content Generation Endpoints

#### POST /api/v2/content/generate/{template_id}

Trigger content generation for template.

**Query Params:**
- `async` (bool, default: true) - Queue for async processing or wait for sync result

**Response (async=true):**
```json
{
  "success": true,
  "job_id": "abc-123-def",
  "status": "queued",
  "message": "Content generation queued successfully"
}
```

**Response (async=false):**
```json
{
  "success": true,
  "content": {
    "id": 42,
    "title": "Security Briefing - 2025-10-02",
    "content_html": "<h1>Executive Summary</h1>...",
    "content_markdown": "# Executive Summary\n...",
    "generated_at": "2025-10-02T10:15:00Z",
    "articles_count": 18,
    "generation_cost_usd": 0.0234,
    "generation_time_seconds": 8
  }
}
```

#### GET /api/v2/content/latest/{template_id}

Get most recent generated content for template.

**Response:**
```json
{
  "success": true,
  "content": {
    "id": 42,
    "template_name": "IT Manager Security Brief",
    "title": "Security Briefing - 2025-10-02",
    "content_html": "...",
    "generated_at": "2025-10-02T08:00:00Z",
    "articles_used": [1234, 1235, 1236]
  }
}
```

### Distribution Endpoints

#### POST /api/v2/distribution/channels/

Add distribution channel to template.

**Request Body:**
```json
{
  "template_id": 1,
  "channel_type": "email",
  "channel_name": "IT Team List",
  "channel_config": {
    "recipients": [
      "it-managers@example.com",
      "security-team@example.com"
    ],
    "subject_template": "🔒 Security Brief - {date}",
    "from_address": "security@news-mcp.com"
  },
  "is_active": true
}
```

**Response:**
```json
{
  "success": true,
  "channel_id": 1,
  "message": "Distribution channel created successfully"
}
```

#### POST /api/v2/distribution/send/{content_id}

Manually trigger distribution for content.

**Request Body:**
```json
{
  "channel_ids": [1, 2, 3]  // Optional, defaults to all active channels
}
```

**Response:**
```json
{
  "success": true,
  "distribution_jobs": [
    {
      "channel_id": 1,
      "channel_name": "IT Team List",
      "status": "sent",
      "recipients": 2
    },
    {
      "channel_id": 2,
      "channel_name": "Web Publication",
      "status": "sent",
      "url": "/briefings/security/2025-10-02"
    }
  ]
}
```

---

## 🧪 Testing Strategy

### Unit Tests

```python
# tests/test_content_generator.py

def test_article_query_builder():
    """Test query builder with various criteria"""
    criteria = {
        "keywords": ["security"],
        "timeframe_hours": 24,
        "min_impact_score": 0.7
    }
    query = build_article_query(criteria)
    assert query is not None
    # More assertions...

def test_llm_prompt_formatting():
    """Test prompt template variable substitution"""
    template = "Brief for {audience} about {topic}"
    result = template.format(audience="IT", topic="Security")
    assert "IT" in result
    assert "Security" in result
```

### Integration Tests

```python
# tests/test_content_generation_integration.py

async def test_end_to_end_generation():
    """Test complete generation workflow"""

    # 1. Create template
    template = await create_template({
        "name": "Test Brief",
        "selection_criteria": {...},
        ...
    })

    # 2. Trigger generation
    job = await trigger_generation(template.id)

    # 3. Wait for completion
    content = await wait_for_job(job.id, timeout=30)

    # 4. Verify content
    assert content is not None
    assert content.articles_count > 0
    assert content.content_html is not None

    # 5. Test distribution
    result = await send_distribution(content.id)
    assert result.status == 'sent'
```

---

## 📚 Use Case Examples

### Use Case 1: IT Manager Security Brief

**Template Configuration:**
```json
{
  "name": "IT Manager Security Brief",
  "target_audience": "IT Management",
  "selection_criteria": {
    "keywords": ["security", "breach", "vulnerability", "CVE", "exploit"],
    "exclude_keywords": ["opinion", "rumor"],
    "timeframe_hours": 24,
    "min_impact_score": 0.6,
    "feed_ids": [1, 5, 8, 12, 15],  // Security-focused feeds
    "max_articles": 30
  },
  "content_structure": {
    "sections": [
      {
        "name": "executive_summary",
        "max_words": 150,
        "prompt": "Summarize the most critical security developments in 2-3 sentences"
      },
      {
        "name": "critical_alerts",
        "format": "list",
        "prompt": "List all high-impact security vulnerabilities requiring immediate attention. Include CVE numbers if available."
      },
      {
        "name": "threat_landscape",
        "max_words": 200,
        "prompt": "Describe emerging threat patterns and attack vectors"
      },
      {
        "name": "recommendations",
        "max_items": 5,
        "prompt": "Provide specific, actionable security recommendations"
      },
      {
        "name": "additional_reading",
        "format": "links",
        "prompt": "Include links to full articles for deeper analysis"
      }
    ],
    "output_format": "markdown"
  },
  "llm_prompt_template": "You are a cybersecurity analyst creating a professional security briefing for IT management...",
  "llm_model": "gpt-4o-mini",
  "generation_schedule": "0 8 * * *",  // Daily at 8am
  "is_active": true
}
```

**Distribution Channels:**
```json
[
  {
    "channel_type": "email",
    "channel_name": "IT Management List",
    "channel_config": {
      "recipients": ["it-managers@company.com"],
      "subject_template": "🔒 Daily Security Brief - {date}",
      "from_address": "security@news-mcp.com"
    }
  },
  {
    "channel_type": "web",
    "channel_name": "Internal Portal",
    "channel_config": {
      "publish_url": "/briefings/security/{date}",
      "access": "private"
    }
  }
]
```

**Expected Output:**
```markdown
# Security Briefing - October 2, 2025

## Executive Summary
Critical vulnerability discovered in OpenSSL affecting millions of servers worldwide (CVE-2025-12345). Major ransomware campaign targeting healthcare organizations continues to escalate. Three zero-day exploits actively used in the wild.

## Critical Alerts
- **CVE-2025-12345** (Impact: 9.8/10) - OpenSSL Remote Code Execution
  - Affects: OpenSSL 3.x versions
  - Action: Immediate patching required
  - Source: OpenSSL Security Advisory

- **Ransomware Campaign** (Impact: 8.5/10) - LockBit 4.0 Targeting Healthcare
  - Affects: Hospital networks, medical devices
  - Action: Review backup procedures, isolate critical systems
  - Source: CISA Alert

[Additional alerts...]

## Threat Landscape
...

## Recommendations
1. Deploy OpenSSL patches within 24 hours
2. Conduct emergency backup verification
3. Review firewall rules for lateral movement prevention
4. Enable enhanced logging for critical systems
5. Schedule security awareness training for Q4

## Additional Reading
- [Full OpenSSL Advisory](https://...)
- [CISA Healthcare Alert](https://...)
```

---

### Use Case 2: Government Policy Update

**Template Configuration:**
```json
{
  "name": "Government Policy Update",
  "target_audience": "Compliance Officers",
  "selection_criteria": {
    "keywords": ["regulation", "policy", "law", "compliance", "government"],
    "timeframe_hours": 48,
    "min_impact_score": 0.5,
    "categories": ["Politics", "Business"],
    "max_articles": 20
  },
  "content_structure": {
    "sections": [
      {
        "name": "summary",
        "max_words": 100
      },
      {
        "name": "new_regulations",
        "format": "list"
      },
      {
        "name": "impact_analysis",
        "max_words": 300
      },
      {
        "name": "compliance_actions",
        "max_items": 10
      }
    ]
  },
  "generation_schedule": "0 0 * * 1",  // Weekly on Monday
  "llm_model": "gpt-4o-mini"
}
```

---

### Use Case 3: Investor Market Intelligence

**Template Configuration:**
```json
{
  "name": "Market Intelligence Brief",
  "target_audience": "Investors",
  "selection_criteria": {
    "keywords": ["market", "stock", "earnings", "merger", "acquisition", "IPO"],
    "timeframe_hours": 6,
    "min_impact_score": 0.7,
    "categories": ["Business", "Finance"],
    "max_articles": 15
  },
  "content_structure": {
    "sections": [
      {
        "name": "market_movers",
        "format": "list",
        "prompt": "Identify stocks with significant price movements and reasons"
      },
      {
        "name": "sentiment_analysis",
        "prompt": "Analyze overall market sentiment (bullish/bearish/neutral)"
      },
      {
        "name": "opportunities",
        "max_items": 5,
        "prompt": "Highlight potential investment opportunities based on news"
      }
    ]
  },
  "generation_schedule": "realtime",  // Generate on new matching articles
  "llm_model": "gpt-4o"  // Premium model for financial analysis
}
```

---

## 🔍 Monitoring & Observability

### Metrics to Track

```python
# Prometheus metrics to add

content_generation_total = Counter(
    'content_generation_total',
    'Total content generations triggered',
    ['template_name', 'status']
)

content_generation_duration_seconds = Histogram(
    'content_generation_duration_seconds',
    'Time to generate content',
    ['template_name']
)

content_generation_cost_usd = Histogram(
    'content_generation_cost_usd',
    'Cost of content generation',
    ['template_name', 'llm_model']
)

distribution_total = Counter(
    'distribution_total',
    'Total distributions sent',
    ['channel_type', 'status']
)

distribution_recipient_count = Histogram(
    'distribution_recipient_count',
    'Number of recipients per distribution',
    ['channel_type']
)
```

### Health Checks

```python
# Add to /api/health/status

{
  "content_generation": {
    "queue_depth": 3,
    "active_jobs": 1,
    "last_generation": "2025-10-02T08:15:00Z",
    "status": "healthy"
  },
  "distribution": {
    "pending_deliveries": 0,
    "last_delivery": "2025-10-02T08:16:00Z",
    "failed_last_24h": 0,
    "status": "healthy"
  }
}
```

---

## 💰 Cost Management

### LLM Cost Estimation

```python
def estimate_generation_cost(template: Template, article_count: int) -> float:
    """
    Estimate OpenAI API cost for content generation.

    Based on:
    - Input tokens (articles + prompt template)
    - Output tokens (expected content length)
    - Model pricing
    """

    # Average article: ~500 tokens
    input_tokens = (article_count * 500) + 1000  # +prompt template

    # Expected output based on content_structure
    output_tokens = sum(
        section.get('max_words', 200) * 1.3  # words to tokens ratio
        for section in template.content_structure['sections']
    )

    # Pricing (gpt-4o-mini)
    cost_per_1k_input = 0.00015
    cost_per_1k_output = 0.0006

    cost = (
        (input_tokens / 1000) * cost_per_1k_input +
        (output_tokens / 1000) * cost_per_1k_output
    )

    return round(cost, 6)
```

### Cost Limits

```python
# Add to .env
MAX_GENERATION_COST_USD=0.50  # Per generation
MAX_DAILY_GENERATION_COST_USD=10.00  # Total per day

# Enforce in worker
if estimated_cost > MAX_GENERATION_COST_USD:
    raise CostLimitExceededError(
        f"Estimated cost ${estimated_cost:.4f} exceeds limit"
    )
```

---

## 🚨 Error Handling

### Generation Failures

```python
class ContentGenerationError(Exception):
    """Base exception for content generation errors"""
    pass

class ArticleQueryError(ContentGenerationError):
    """No articles found matching criteria"""
    pass

class LLMOutputInvalidError(ContentGenerationError):
    """LLM output doesn't match expected schema"""
    pass

class CostLimitExceededError(ContentGenerationError):
    """Generation would exceed cost limits"""
    pass

# Retry logic
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(LLMOutputInvalidError)
)
async def generate_with_retry(template_id: int):
    """Generate content with retry on validation failures"""
    pass
```

### Distribution Failures

```python
class DistributionError(Exception):
    """Base exception for distribution errors"""
    pass

class EmailDeliveryError(DistributionError):
    """Email failed to send"""
    pass

class WebPublicationError(DistributionError):
    """Failed to publish to web"""
    pass

# Dead letter queue for permanent failures
async def handle_distribution_failure(
    content_id: int,
    channel_id: int,
    error: Exception
):
    """
    Handle distribution failures:
    1. Log to distribution_log
    2. Retry up to 3 times
    3. After 3 failures, move to dead letter queue
    4. Alert admin
    """
    pass
```

---

## 📖 Documentation TODO

### User Documentation
- [ ] Template creation guide
- [ ] Best practices for prompt engineering
- [ ] Selection criteria examples
- [ ] Distribution channel setup guide
- [ ] Troubleshooting guide

### Developer Documentation
- [ ] Architecture diagram
- [ ] Database schema documentation
- [ ] API reference (OpenAPI spec)
- [ ] Worker implementation guide
- [ ] Extension guide (adding new channel types)

---

## 🎯 Success Criteria

### Technical Success
- [ ] All database migrations run successfully
- [ ] All API endpoints functional and tested
- [ ] Content generator worker processes jobs correctly
- [ ] Distribution channels deliver reliably (>99% success rate)
- [ ] System handles 100+ templates without performance degradation
- [ ] Generation latency < 30 seconds average
- [ ] No data loss or corruption

### Business Success
- [ ] 1 complete use case (Security Brief) operational
- [ ] Email distribution working end-to-end
- [ ] Web publication accessible and formatted correctly
- [ ] Scheduled generation runs reliably
- [ ] Cost per generation < $0.10 average
- [ ] User can create template through UI in < 10 minutes
- [ ] Documentation complete and clear

---

## 📅 Development Log

See [DEVELOPMENT_LOG.md](./DEVELOPMENT_LOG.md) for daily progress tracking.

---

## 🤝 Resources & Support

### External Dependencies
- OpenAI API (existing)
- SMTP server (needs setup - MailHog for dev?)
- Jinja2 (already installed)
- feedgen (for RSS - `pip install feedgen`)

### Development Tools
- Database: PostgreSQL (existing)
- Testing: pytest (existing)
- API Testing: curl/httpx
- Email Testing: MailHog (local SMTP server)

### Questions/Blockers
None yet - will track in development log

---

**Last Updated:** 2025-10-02
**Version:** 1.0
**Status:** Ready to begin Phase 1
