"""add conversations and messages

Revision ID: 1bde0ba04aa0
Revises: a2c7e547af5a
Create Date: 2026-09-11 15:20:15.197835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bde0ba04aa0'
down_revision: Union[str, Sequence[str], None] = 'a2c7e547af5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_unique_constraint(
        "uq_users_id_org_id",
        "users",
        ["id", "org_id"],
    )

    op.create_table(
        "conversations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("org_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id", "org_id"],
            ["users.id", "users.org_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("conversation_id", sa.Integer(), nullable=False),
        sa.Column(
            "role",
            sa.Enum(
                "user",
                "assistant",
                "system",
                name="message_role",
            ),
            nullable=False,
        ),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["conversation_id"],
            ["conversations.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("messages")
    op.drop_table("conversations")

    op.drop_constraint(
        "uq_users_id_org_id",
        "users",
        type_="unique",
    )