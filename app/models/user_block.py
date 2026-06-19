from datetime import datetime, timedelta, timezone
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.db_instance import db

class UserBlock(db.Model):
    __tablename__ = 'user_blocks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    blocked_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    unlocked_at = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="blocks_received")
    
    @classmethod
    def block_user(cls, user, block_duration_minutes=15):
        try:
            now = datetime.now(timezone.utc)
            block = cls(
                user_id=user.id,
                blocked_at=now,
                unlocked_at=now + timedelta(minutes=block_duration_minutes)
            )
            
            db.session.add(block)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Error blocking user: {str(e)}")

        return block
    
    @classmethod
    def get_block_by_user(cls, user):
        try:
            now = datetime.now(timezone.utc)
            block = cls.query.filter(
                cls.user_id == user.id,
                cls.unlocked_at > now
            ).first()
            
            if block:
                return int(block.unlocked_at - now).total_seconds() // 60 + 1
            return None
        
        except Exception as e:
            return None