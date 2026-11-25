"""Database models for PassportPal."""

from datetime import date, datetime
from typing import Any

from sqlalchemy import (
    JSON,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy import (
    text as sql_text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# Supports SQLite for local tests and PostgreSQL JSONB in production.
json_type = JSON().with_variant(JSONB(), "postgresql")


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


class Document(Base):
    """Stores uploaded and processed documents."""

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    external_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)

    title: Mapped[str] = mapped_column(Text, nullable=False)

    source_url: Mapped[str | None] = mapped_column(Text)

    licence: Mapped[str | None] = mapped_column(String(200))

    doc_type: Mapped[str] = mapped_column(String(50), nullable=False, server_default="record")

    published_on: Mapped[date | None] = mapped_column(Date)

    sha256: Mapped[str] = mapped_column(String(64), nullable=False)

    metadata_: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        json_type,
        nullable=False,
        server_default=sql_text("'{}'"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    pages: Mapped[list["Page"]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "external_id",
            name="uq_documents_external_id",
        ),
        Index("ix_documents_doc_type", "doc_type"),
        Index("ix_documents_sha256", "sha256"),
        Index(
            "ix_documents_metadata_gin",
            "metadata",
            postgresql_using="gin",
            postgresql_ops={"metadata": "jsonb_path_ops"},
        ).ddl_if(dialect="postgresql"),
    )


class Page(Base):
    """Stores extracted text and headings for each document page."""

    __tablename__ = "pages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    document_id: Mapped[int] = mapped_column(
        ForeignKey(
            "documents.id",
            ondelete="CASCADE",
            name="fk_pages_document_id_documents",
        ),
        nullable=False,
    )

    page_no: Mapped[int] = mapped_column(Integer, nullable=False)

    text: Mapped[str] = mapped_column(Text, nullable=False)

    headings: Mapped[list[Any]] = mapped_column(
        json_type,
        nullable=False,
        server_default=sql_text("'[]'"),
    )

    document: Mapped["Document"] = relationship(back_populates="pages")

    __table_args__ = (
        CheckConstraint(
            "page_no >= 1",
            name="ck_pages_page_no_positive",
        ),
        UniqueConstraint(
            "document_id",
            "page_no",
            name="uq_pages_document_page",
        ),
        Index("ix_pages_document_id", "document_id"),
    )


class ParseFailure(Base):
    """Tracks documents that failed during parsing."""

    __tablename__ = "parse_failures"

    path: Mapped[str] = mapped_column(Text, primary_key=True)

    sha256: Mapped[str] = mapped_column(String(64), nullable=False)

    source_url: Mapped[str | None] = mapped_column(Text)

    reason: Mapped[str] = mapped_column(String(100), nullable=False)

    detail: Mapped[str] = mapped_column(Text, nullable=False)

    attempts: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=sql_text("1"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class LlmCall(Base):
    """Tracks language model calls, usage, latency and cost."""

    __tablename__ = "llm_calls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    request_id: Mapped[str] = mapped_column(String(64), index=True)

    provider: Mapped[str] = mapped_column(String(40))

    model: Mapped[str] = mapped_column(String(80))

    purpose: Mapped[str] = mapped_column(String(40), server_default="chat")

    prompt_version: Mapped[str] = mapped_column(String(80), server_default="")

    status: Mapped[str] = mapped_column(String(10))

    error: Mapped[str] = mapped_column(Text, server_default="")

    tokens_in: Mapped[int] = mapped_column(server_default="0")

    tokens_out: Mapped[int] = mapped_column(server_default="0")

    latency_ms: Mapped[int] = mapped_column(server_default="0")

    cost_inr: Mapped[float] = mapped_column(Numeric(12, 6), server_default="0")

    fallback_used: Mapped[bool] = mapped_column(server_default=sql_text("false"))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )
