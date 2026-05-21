from sqlalchemy.orm import Session
from app.models.meeting import Meeting
from app.schemas.meeting import MeetingCreate, MeetingUpdate


def get_meeting(db: Session, meeting_id: int):
    """Get a meeting by ID."""
    return db.query(Meeting).filter(Meeting.id == meeting_id).first()


def get_all_meetings(db: Session, skip: int = 0, limit: int = 10):
    """Get all meetings with pagination."""
    return db.query(Meeting).offset(skip).limit(limit).all()


def create_meeting(db: Session, meeting: MeetingCreate):
    """Create a new meeting."""
    db_meeting = Meeting(
        title=meeting.title,
        description=meeting.description,
        participants=meeting.participants,
        duration_minutes=meeting.duration_minutes
    )
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting


def update_meeting(db: Session, meeting_id: int, meeting_update: MeetingUpdate):
    """Update an existing meeting."""
    db_meeting = get_meeting(db, meeting_id)
    if not db_meeting:
        return None
    
    update_data = meeting_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_meeting, key, value)
    
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting


def delete_meeting(db: Session, meeting_id: int):
    """Delete a meeting."""
    db_meeting = get_meeting(db, meeting_id)
    if db_meeting:
        db.delete(db_meeting)
        db.commit()
    return db_meeting
