# backend/app/users/models.py
import uuid
from sqlalchemy import Column, String, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from backend.app.database.base import Base


class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # References auth.users.id — NOT a SQLAlchemy ForeignKey, since that table
    # lives in Supabase's managed "auth" schema (don't build FKs against it;
    # Supabase's own docs warn against depending on that schema's structure).
    user_id = Column(UUID(as_uuid=True), unique=True, nullable=False, index=True)
    favorite_topics = Column(ARRAY(String), default=list)
    blocked_topics = Column(ARRAY(String), default=list)
    preferred_sources = Column(ARRAY(String), default=list)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())