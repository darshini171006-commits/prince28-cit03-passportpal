"""create parse failures table

Revision ID: c7f2a91d6e40
Revises: a448661aebe1
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "c7f2a91d6e40"  # pragma: allowlist secret
down_revision: str | None = "a448661aebe1"  # pragma: allowlist secret
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "parse_failures",
        sa.Column("path", sa.Text(), nullable=False),
        sa.Column("sha256", sa.String(length=64), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("reason", sa.String(length=100), nullable=False),
        sa.Column("detail", sa.Text(), nullable=False),
        sa.Column(
            "attempts",
            sa.Integer(),
            server_default=sa.text("1"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint(
            "path",
            name=op.f("pk_parse_failures"),
        ),
    )


def downgrade() -> None:
    op.drop_table("parse_failures")
