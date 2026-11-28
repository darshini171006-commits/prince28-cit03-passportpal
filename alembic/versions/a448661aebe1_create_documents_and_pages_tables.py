"""create documents and pages tables

Revision ID: a448661aebe1
Revises:
Create Date: 2026-11-22 19:53:19.173947
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "a448661aebe1"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()

    json_type = sa.JSON().with_variant(
        postgresql.JSONB(),
        "postgresql",
    )

    op.create_table(
        "documents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("external_id", sa.String(length=64), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("licence", sa.String(length=200), nullable=True),
        sa.Column(
            "doc_type",
            sa.String(length=50),
            server_default="record",
            nullable=False,
        ),
        sa.Column("published_on", sa.Date(), nullable=True),
        sa.Column("sha256", sa.String(length=64), nullable=False),
        sa.Column(
            "metadata",
            json_type,
            server_default=sa.text("'{}'"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_documents")),
        sa.UniqueConstraint(
            "external_id",
            name=op.f("uq_documents_external_id"),
        ),
    )

    op.create_index(
        "ix_documents_doc_type",
        "documents",
        ["doc_type"],
        unique=False,
    )

    if bind.dialect.name == "postgresql":
        op.create_index(
            "ix_documents_metadata_gin",
            "documents",
            ["metadata"],
            unique=False,
            postgresql_using="gin",
            postgresql_ops={"metadata": "jsonb_path_ops"},
        )

    op.create_index(
        op.f("ix_documents_sha256"),
        "documents",
        ["sha256"],
        unique=False,
    )

    op.create_table(
        "pages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("page_no", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.CheckConstraint(
            "page_no >= 1",
            name=op.f("ck_pages_page_no_positive"),
        ),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["documents.id"],
            name=op.f("fk_pages_document_id_documents"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_pages")),
        sa.UniqueConstraint(
            "document_id",
            "page_no",
            name="uq_pages_document_page",
        ),
    )

    op.create_index(
        op.f("ix_pages_document_id"),
        "pages",
        ["document_id"],
        unique=False,
    )


def downgrade() -> None:
    bind = op.get_bind()

    op.drop_index(
        op.f("ix_pages_document_id"),
        table_name="pages",
    )
    op.drop_table("pages")

    op.drop_index(
        op.f("ix_documents_sha256"),
        table_name="documents",
    )

    if bind.dialect.name == "postgresql":
        op.drop_index(
            "ix_documents_metadata_gin",
            table_name="documents",
        )

    op.drop_index(
        "ix_documents_doc_type",
        table_name="documents",
    )
    op.drop_table("documents")
