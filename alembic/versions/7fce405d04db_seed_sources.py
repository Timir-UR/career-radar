"""seed sources

Revision ID: 7fce405d04db
Revises: 3b484da95ae9
Create Date: 2026-08-28 15:34:14.888528

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7fce405d04db"
down_revision: Union[str, Sequence[str], None] = "3b484da95ae9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        INSERT INTO sources (name, type, base_url, enabled)
        VALUES
            ('remotive', 'api', 'https://remotive.com/api/remote-jobs', true)
        ON CONFLICT (name) DO NOTHING
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        DELETE FROM sources WHERE name = 'remotive'
        """
    )
