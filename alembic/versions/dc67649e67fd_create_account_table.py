"""create account table

Revision ID: dc67649e67fd
Revises: feee59097a2b
Create Date: 2025-09-15 18:36:52.522316

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc67649e67fd'
down_revision: Union[str, Sequence[str], None] = 'feee59097a2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
