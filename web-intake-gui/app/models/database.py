"""SQLAlchemy database models."""

from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Boolean,
    Integer,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class ReportDB(Base):
    """Database model for reports."""

    __tablename__ = "reports"

    id = Column(String(32), primary_key=True)
    report_type = Column(String(50), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    organization = Column(String(200), nullable=False)
    classification = Column(String(20), nullable=False, default="INTERNAL")

    # Content stored as JSON
    content_markdown = Column(Text, nullable=False)
    content_html = Column(Text, nullable=True)
    content_raw_data = Column(JSON, nullable=True)

    # Metadata stored as JSON
    metadata_json = Column(JSON, nullable=True)

    generated_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    share_links = relationship(
        "ShareLinkDB", back_populates="report", cascade="all, delete-orphan"
    )


class ShareLinkDB(Base):
    """Database model for share links."""

    __tablename__ = "share_links"

    id = Column(String(32), primary_key=True)
    report_id = Column(String(32), ForeignKey("reports.id"), nullable=False, index=True)
    token = Column(String(48), unique=True, nullable=False, index=True)
    password_hash = Column(String(128), nullable=True)
    allow_download = Column(Boolean, nullable=False, default=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    view_count = Column(Integer, nullable=False, default=0)

    # Relationships
    report = relationship("ReportDB", back_populates="share_links")
