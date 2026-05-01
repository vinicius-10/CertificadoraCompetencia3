#docker-compose exec web flask db migrate -m "descricao"
#docker-compose exec web flask db upgrade



from datetime import datetime
import enum
from sqlalchemy import Enum as SAEnum
import uuid
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from argon2 import PasswordHasher




ph = PasswordHasher()
db = SQLAlchemy()
# --- Enums para a tabela USERS ---
class UserProfile(enum.Enum):
    COORDINATOR  = "Coordenador(a)"
    ADMIN  = "Admin"
    VOLUNTEER  = "Voluntário(a)"

class UserStatus(enum.Enum):
    ACTIVE = "Ativo"
    INACTIVE = "Desligado"
    DELETED = "Excluído"

class UserMarital(enum.Enum):
    SINGLE  = "Solteiro(a)"
    MARRIED  = "Casado(a)"
    DIVORCED  = "Divorciado(a)"
    WIDOWED  = "Viúvo(a)"
    STABLE_UNION = "União Estável"     
    

# --- Tabelas ---

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    use_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ra = Column(String(20), unique=True, nullable=False)
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
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    update_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def set_password(self, password):
        self.password_hash = ph.hash(password)
        
    def check_password(self, password):
        try:
            return ph.verify(self.password_hash, password)
        except:
            return False    

    # Relacionamentos
    address = relationship("Address", back_populates="user", uselist=False)
    
    status_history = relationship("StatusHistory", foreign_keys="[StatusHistory.user_id]")
    changes_made = relationship("StatusHistory", foreign_keys="[StatusHistory.changed_by_user_id]")
    
    logs = relationship("AccessLog", back_populates="user")
    
    recovery_tokens = relationship("PasswordRecoveryToken", back_populates="user")
    
    blocks_received = relationship("UserBlock", back_populates="user")


class Address(db.Model):
    __tablename__ = 'address'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.use_id'), nullable=False)
    postal_code = Column(String(8), nullable=False)
    street = Column(String(150), nullable=False)
    number = Column(String(20), nullable=False)
    complement = Column(String(100), nullable=True)
    neighborhood = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(50), default='Brasil', nullable=False)

    user = relationship("User", back_populates="address")

class StatusHistory(db.Model):
    __tablename__ = 'status_history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.use_id'), nullable=False)
    changed_by_user_id = Column(UUID(as_uuid=True), ForeignKey('users.use_id'), nullable=False)
    previous_status = Column(Enum(UserStatus), nullable=False)
    new_status = Column(Enum(UserStatus), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class AccessLog(db.Model):
    __tablename__ = 'access_logs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.use_id'), nullable=False)
    accessed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_successful = Column(Boolean, nullable=False)

    user = relationship("User", back_populates="logs")

class PasswordRecoveryToken(db.Model):
    __tablename__ = 'password_recovery_tokens'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.use_id'), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="recovery_tokens")

class UserBlock(db.Model):
    __tablename__ = 'user_blocks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.use_id'), nullable=False)
    blocked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    desbloqueio_em = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="blocks_received")