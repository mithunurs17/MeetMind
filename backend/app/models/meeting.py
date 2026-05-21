from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base


class Meeting(Base):
    """Meeting model for storing meeting information."""
    
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    participants = Column(JSON, nullable=True)  # List of participant names
    minutes = Column(Text, nullable=True)  # Meeting minutes
    action_items = Column(JSON, nullable=True)  # List of action items
    recording_path = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    class Config:
        from_attributes = True
