from datetime import datetime, timedelta, timezone
import uuid
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.db_instance import db

class AccessLog(db.Model):
    __tablename__ = 'access_logs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    attempted__user = Column(String(255), nullable=False)
    accessed_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    is_successful = Column(Boolean, nullable=False)

    user = relationship("User", back_populates="logs")
    
    @classmethod
    def register_attempt(cls, user=None, username_attempt="", is_successful=False):
        try:
            log = cls(
                user_id=user.id if user else None,
                attempted__user=username_attempt,
                is_successful=is_successful
            )
            
            db.session.add(log)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Error recording log: {str(e)}")

        return log
    
    @classmethod
    def count_access_attempts(cls, username, within_minutes=15):
        try:
            time_threshold = datetime.now(timezone.utc) - timedelta(minutes=within_minutes)
            print(f"\n\n verificando tentativas para {username} desde {time_threshold}\n\n",flush=True)
            return cls.query.filter(
                cls.attempted__user == username,
                cls.accessed_at >= time_threshold,
                cls.is_successful == False
            ).count()
        except Exception as e:
            return 0
