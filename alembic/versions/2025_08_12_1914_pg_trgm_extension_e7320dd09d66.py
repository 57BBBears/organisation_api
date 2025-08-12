"""pg_trgm extension

Revision ID: e7320dd09d66
Revises: 086db8a8858a
Create Date: 2025-08-12 19:14:46.112251

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "e7320dd09d66"
down_revision: Union[str, Sequence[str], None] = "086db8a8858a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP EXTENSION IF EXISTS pg_trgm")
