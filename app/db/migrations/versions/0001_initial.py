"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2025-12-06 00:00:00.000000
"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create all tables using SQLAlchemy metadata."""
    bind = op.get_bind()
    # Importing here to ensure models are loaded and registered on metadata
    from app.db.base import Base

    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    bind = op.get_bind()
    from app.db.base import Base

    Base.metadata.drop_all(bind=bind)
