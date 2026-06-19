from app.models.db_instance import db
from app.models.enums import UserProfile, UserStatus, UserMarital

from argon2 import PasswordHasher
from sqlalchemy import Enum as SAEnum
import uuid
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from argon2 import PasswordHasher
from datetime import datetime, timezone


ph = PasswordHasher()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code_institutional = Column(String(20), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(150), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    cpf = Column(String(255), unique=True, nullable=False)
    rg = Column(String(255),  unique=True, nullable=False)
    nationality = Column(String(50), nullable=False)
    marital = Column(SAEnum(UserMarital, values_callable=lambda x: [e.value for e in x]), nullable=True)
    profession = Column(String(100), nullable=True)
    profile = Column(SAEnum(UserProfile, values_callable=lambda x: [e.value for e in x]), nullable=False)
    status = Column(SAEnum(UserStatus, values_callable=lambda x: [e.value for e in x]), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    update_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    # Relacionamentos
    address = relationship("Address", back_populates="user", uselist=False)
    
    status_history = relationship("StatusHistory", foreign_keys="[StatusHistory.user_id]")
    changes_made = relationship("StatusHistory", foreign_keys="[StatusHistory.changed_by_user_id]")
    
    logs = relationship("AccessLog", back_populates="user")
    
    recovery_tokens = relationship("PasswordRecoveryToken", back_populates="user")
    
    blocks_received = relationship("UserBlock", back_populates="user")
    
    def set_password(self, password):
        self.password_hash = ph.hash(password)
        
    def check_password(self, password):
        try:
            return ph.verify(self.password_hash, password)
        except:
            return False    
