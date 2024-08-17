"""Add random_field field into users table

Revision ID: 0000002
Revises: 0000001
Create Date: 2024-07-30 21:51:26.311409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0000002'
down_revision: Union[str, None] = '0000001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('random_field', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'random_field')