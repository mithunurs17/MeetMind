from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class MeetingCreate(BaseModel):
    """Schema for creating a new meeting."""
    title: str
    description: Optional[str] = None
    participants: Optional[List[str]] = None
    duration_minutes: Optional[int] = None


class MeetingUpdate(BaseModel):
    """Schema for updating a meeting."""
    title: Optional[str] = None
    description: Optional[str] = None
    minutes: Optional[str] = None
    action_items: Optional[List[dict]] = None
    duration_minutes: Optional[int] = None


class MeetingResponse(BaseModel):
    """Schema for meeting response."""
    id: int
    title: str
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    participants: Optional[List[str]] = None
    minutes: Optional[str] = None
    action_items: Optional[List[dict]] = None
    recording_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
