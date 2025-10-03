"""add content distribution system tables

Revision ID: 3f1e428c6eee
Revises: geopolitical_001
Create Date: 2025-10-02 18:51:56.834743

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f1e428c6eee'
down_revision: Union[str, Sequence[str], None] = 'geopolitical_001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Add content distribution system tables."""

    # Table 1: content_templates
    op.create_table(
        'content_templates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('target_audience', sa.String(length=100), nullable=True),

        # Selection criteria (JSONB)
        sa.Column('selection_criteria', sa.dialects.postgresql.JSONB(), nullable=False),

        # Content structure (JSONB)
        sa.Column('content_structure', sa.dialects.postgresql.JSONB(), nullable=False),

        # LLM configuration
        sa.Column('llm_prompt_template', sa.Text(), nullable=False),
        sa.Column('llm_model', sa.String(length=50), nullable=False, server_default='gpt-4o-mini'),
        sa.Column('llm_temperature', sa.Numeric(precision=3, scale=2), nullable=False, server_default='0.7'),

        # Scheduling
        sa.Column('generation_schedule', sa.String(length=100), nullable=True),

        # Status
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),

        # Metadata
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('tags', sa.dialects.postgresql.JSONB(), nullable=True),

        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name', name='uq_template_name')
    )

    # Indexes for content_templates
    op.create_index('idx_templates_active', 'content_templates', ['is_active'])
    op.create_index('idx_templates_schedule', 'content_templates', ['generation_schedule'])

    # Table 2: generated_content
    op.create_table(
        'generated_content',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('template_id', sa.Integer(), nullable=False),

        # Generated content
        sa.Column('title', sa.String(length=500), nullable=True),
        sa.Column('content_html', sa.Text(), nullable=True),
        sa.Column('content_markdown', sa.Text(), nullable=True),
        sa.Column('content_json', sa.dialects.postgresql.JSONB(), nullable=True),

        # Metadata
        sa.Column('generated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('generation_job_id', sa.String(length=100), nullable=True),

        # Source tracking
        sa.Column('source_article_ids', sa.dialects.postgresql.ARRAY(sa.Integer()), nullable=False),
        sa.Column('articles_count', sa.Integer(), nullable=False),

        # Quality metrics
        sa.Column('word_count', sa.Integer(), nullable=True),
        sa.Column('generation_cost_usd', sa.Numeric(precision=10, scale=6), nullable=True),
        sa.Column('generation_time_seconds', sa.Integer(), nullable=True),
        sa.Column('llm_model_used', sa.String(length=50), nullable=True),

        # Status
        sa.Column('status', sa.String(length=20), nullable=False, server_default='generated'),
        sa.Column('published_at', sa.DateTime(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),

        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['template_id'], ['content_templates.id'], ondelete='CASCADE')
    )

    # Indexes for generated_content
    op.create_index('idx_content_template', 'generated_content', ['template_id'])
    op.create_index('idx_content_generated_at', 'generated_content', ['generated_at'], postgresql_ops={'generated_at': 'DESC'})
    op.create_index('idx_content_status', 'generated_content', ['status'])

    # Table 3: distribution_channels
    op.create_table(
        'distribution_channels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('template_id', sa.Integer(), nullable=False),

        # Channel configuration
        sa.Column('channel_type', sa.String(length=20), nullable=False),
        sa.Column('channel_name', sa.String(length=200), nullable=False),
        sa.Column('channel_config', sa.dialects.postgresql.JSONB(), nullable=False),

        # Status
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('last_used_at', sa.DateTime(), nullable=True),

        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['template_id'], ['content_templates.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('template_id', 'channel_type', 'channel_name', name='uq_channel_per_template')
    )

    # Indexes for distribution_channels
    op.create_index('idx_channels_template', 'distribution_channels', ['template_id'])
    op.create_index('idx_channels_type', 'distribution_channels', ['channel_type'])
    op.create_index('idx_channels_active', 'distribution_channels', ['is_active'])

    # Table 4: distribution_log
    op.create_table(
        'distribution_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content_id', sa.Integer(), nullable=False),
        sa.Column('channel_id', sa.Integer(), nullable=False),

        # Distribution status
        sa.Column('status', sa.String(length=20), nullable=False, server_default='pending'),
        sa.Column('sent_at', sa.DateTime(), nullable=True),

        # Delivery details
        sa.Column('recipient_count', sa.Integer(), nullable=True),
        sa.Column('recipients_list', sa.dialects.postgresql.JSONB(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('retry_count', sa.Integer(), nullable=False, server_default='0'),

        # Tracking (optional)
        sa.Column('open_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('click_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('tracking_enabled', sa.Boolean(), nullable=False, server_default='false'),

        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),

        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['content_id'], ['generated_content.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['channel_id'], ['distribution_channels.id'], ondelete='CASCADE')
    )

    # Indexes for distribution_log
    op.create_index('idx_distlog_content', 'distribution_log', ['content_id'])
    op.create_index('idx_distlog_channel', 'distribution_log', ['channel_id'])
    op.create_index('idx_distlog_status', 'distribution_log', ['status'])
    op.create_index('idx_distlog_sent_at', 'distribution_log', ['sent_at'], postgresql_ops={'sent_at': 'DESC'})

    # Table 5: pending_content_generation (Queue)
    op.create_table(
        'pending_content_generation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('template_id', sa.Integer(), nullable=False),

        # Queue status
        sa.Column('status', sa.String(length=20), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),

        # Processing info
        sa.Column('worker_id', sa.String(length=100), nullable=True),
        sa.Column('generated_content_id', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('retry_count', sa.Integer(), nullable=False, server_default='0'),

        # Metadata
        sa.Column('triggered_by', sa.String(length=50), nullable=False, server_default='manual'),

        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['template_id'], ['content_templates.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['generated_content_id'], ['generated_content.id'], ondelete='SET NULL')
    )

    # Indexes for pending_content_generation
    op.create_index('idx_pending_generation_status', 'pending_content_generation', ['status'])
    op.create_index('idx_pending_generation_created', 'pending_content_generation', ['created_at'])
    op.create_index('idx_pending_generation_template', 'pending_content_generation', ['template_id'])


def downgrade() -> None:
    """Downgrade schema - Remove content distribution system tables."""

    # Drop tables in reverse order (respect foreign keys)
    op.drop_index('idx_pending_generation_template', table_name='pending_content_generation')
    op.drop_index('idx_pending_generation_created', table_name='pending_content_generation')
    op.drop_index('idx_pending_generation_status', table_name='pending_content_generation')
    op.drop_table('pending_content_generation')

    op.drop_index('idx_distlog_sent_at', table_name='distribution_log')
    op.drop_index('idx_distlog_status', table_name='distribution_log')
    op.drop_index('idx_distlog_channel', table_name='distribution_log')
    op.drop_index('idx_distlog_content', table_name='distribution_log')
    op.drop_table('distribution_log')

    op.drop_index('idx_channels_active', table_name='distribution_channels')
    op.drop_index('idx_channels_type', table_name='distribution_channels')
    op.drop_index('idx_channels_template', table_name='distribution_channels')
    op.drop_table('distribution_channels')

    op.drop_index('idx_content_status', table_name='generated_content')
    op.drop_index('idx_content_generated_at', table_name='generated_content')
    op.drop_index('idx_content_template', table_name='generated_content')
    op.drop_table('generated_content')

    op.drop_index('idx_templates_schedule', table_name='content_templates')
    op.drop_index('idx_templates_active', table_name='content_templates')
    op.drop_table('content_templates')
