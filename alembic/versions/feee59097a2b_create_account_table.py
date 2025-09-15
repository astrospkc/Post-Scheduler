"""create account table

Revision ID: feee59097a2b
Revises: 4ffa37053114
Create Date: 2025-09-15 18:32:17.326629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'feee59097a2b'
down_revision: Union[str, Sequence[str], None] = '4ffa37053114'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
