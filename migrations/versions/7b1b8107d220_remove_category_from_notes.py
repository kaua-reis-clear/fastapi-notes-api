"""Remove category from notes

Revision ID: 7b1b8107d220
Revises: b0f46780ceec
Create Date: 2025-05-02 10:15:29.186966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b1b8107d220'
down_revision: Union[str, None] = 'b0f46780ceec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notes', 'category')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notes', sa.Column('category', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
