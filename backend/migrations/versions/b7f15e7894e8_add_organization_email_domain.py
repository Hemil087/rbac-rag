"""add organization email domain

Revision ID: b7f15e7894e8
Revises: 50ec87894725
Create Date: 2026-09-11 19:06:11.959178

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7f15e7894e8'
down_revision: Union[str, Sequence[str], None] = '50ec87894725'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add the column temporarily as nullable
    op.add_column(
        "organizations",
        sa.Column(
            "email_domain",
            sa.String(length=255),
            nullable=True,
        ),
    )

    # 2. Populate existing organizations
    op.execute(
        """
        UPDATE organizations
        SET email_domain = CASE
            WHEN name = 'Acme Corporation' THEN 'acme.com'
            WHEN name = 'Globex Corporation' THEN 'globex.com'
            WHEN name = 'Company B' THEN 'companyb.com'
        END
        """
    )

    # 3. Make sure every existing row received a domain
    #    before enforcing NOT NULL
    op.alter_column(
        "organizations",
        "email_domain",
        nullable=False,
    )

    # 4. Enforce uniqueness
    op.create_unique_constraint(
        "uq_organizations_email_domain",
        "organizations",
        ["email_domain"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_organizations_email_domain",
        "organizations",
        type_="unique",
    )

    op.drop_column(
        "organizations",
        "email_domain",
    )