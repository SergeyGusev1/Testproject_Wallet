"""empty message

Revision ID: 882fa418bc76
Revises: 3d7f483502b9
Create Date: 2026-02-22 15:55:18.118174

"""
from typing import Sequence, Union



# revision identifiers, used by Alembic.
revision: str = '882fa418bc76'
down_revision: Union[str, Sequence[str], None] = '3d7f483502b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
