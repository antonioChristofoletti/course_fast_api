"""First commit

Revision ID: 0000001
Revises:
Create Date: 2024-07-30 14:14:39.717432

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0000001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("role", sa.String(), nullable=True),
        sa.Column("phone_number", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )

    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    op.create_table(
        "todos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("priority", sa.Integer(), nullable=True),
        sa.Column("complete", sa.Boolean(), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(op.f("ix_todos_id"), "todos", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_todos_id"), table_name="todos")
    op.drop_table("todos")

    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
