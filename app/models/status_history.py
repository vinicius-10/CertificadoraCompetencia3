from datetime import datetime, timedelta, timezone
import uuid
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from app.models.enums import UserStatus

from app.models.db_instance import db

class StatusHistory(db.Model):
    __tablename__ = 'status_history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    changed_by_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    previous_status = Column(Enum(UserStatus), nullable=False)
    new_status = Column(Enum(UserStatus), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)