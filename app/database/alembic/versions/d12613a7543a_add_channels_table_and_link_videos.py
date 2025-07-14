"""Add channels table and link videos

Revision ID: d12613a7543a
Revises: 2e6e89f774eb
Create Date: 2025-07-15 04:22:21.552473

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd12613a7543a'
down_revision: Union[str, Sequence[str], None] = '2e6e89f774eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
