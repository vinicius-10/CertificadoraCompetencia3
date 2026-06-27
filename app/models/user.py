"""User model and validation helpers used by authentication and administration."""

import uuid
from datetime import datetime, timezone

from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error
from email_validator import EmailNotValidError, validate_email
from flask_login import UserMixin
from sqlalchemy import Column, DateTime, Enum as SAEnum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from unidecode import unidecode

from app.models import db
from app.models.enums import UserMarital, UserPosition, UserProfile, UserSector, UserStatus


ph = PasswordHasher()


class User(db.Model, UserMixin):
    """
    Represents an application user.

    The model stores personal, institutional, authentication, status, and
    profile information. It also owns helpers for password hashing, CPF/email/RG
    validation, safe serialization, and status transitions used by services and
    routes.
    """

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
    sector = Column(SAEnum(UserSector, values_callable=lambda x: [e.value for e in x]), nullable=True)
    position = Column(SAEnum(UserPosition, values_callable=lambda x: [e.value for e in x]), nullable=True)
    profile = Column(SAEnum(UserProfile, values_callable=lambda x: [e.value for e in x]), nullable=False)
    status = Column(SAEnum(UserStatus, values_callable=lambda x: [e.value for e in x]), nullable=False)
    entry_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    departure_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    update_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relacionamentos
    address = relationship("Address", back_populates="user", uselist=False)
    
    status_history = relationship("StatusHistory", foreign_keys="[StatusHistory.user_id]")
    changes_made = relationship("StatusHistory", foreign_keys="[StatusHistory.changed_by_user_id]")
    
    logs = relationship("AccessLog", back_populates="user")
    
    recovery_tokens = relationship("PasswordRecoveryToken", back_populates="user")
    
    blocks_received = relationship("UserBlock", back_populates="user")
    
    def __init__(self, **kwargs):
        """
        Initializes a user and creates a default password when none is provided.

        The default password is generated from the first and last name. This
        behavior keeps compatibility with the current registration flow, where
        new users are created without an explicit password.

        Args:
            **kwargs: SQLAlchemy model attributes used to create the user.
        """
        super(User, self).__init__(**kwargs)
        
        if self.password_hash is None:
            self._set_default_password()

    def __repr__(self) -> str:
        """
        Returns a concise representation for logs and debugging.

        Sensitive fields such as password hash, CPF, and RG are intentionally
        omitted from this representation.

        Returns:
            str: Debug-friendly user representation.
        """
        return f"<User id={self.id} email={self.email} profile={self.profile} status={self.status}>"

    def __str__(self) -> str:
        """
        Returns a human-readable user description.

        Returns:
            str: User name and email.
        """
        return f"{self.name} <{self.email}>"
    
    def set_password(self, password):
        """
        Hashes and stores a plain-text password.

        Args:
            password (str): Plain-text password to hash.
        """
        self.password_hash = ph.hash(password)
        
    def check_password(self, password):
        """
        Verifies whether a plain-text password matches the stored hash.

        Args:
            password (str): Plain-text password submitted by the user.

        Returns:
            bool: True when the password is valid; otherwise, False.
        """
        try:
            return ph.verify(self.password_hash, password)
        except Argon2Error:
            return False

    @property
    def is_active(self) -> bool:
        """
        Indicates whether the user can authenticate with Flask-Login.

        Returns:
            bool: True when the user status is active; otherwise, False.
        """
        return self.status == UserStatus.ACTIVE

    @property
    def is_inactive(self) -> bool:
        """
        Indicates whether the user is marked as inactive.

        Returns:
            bool: True when the user status is inactive; otherwise, False.
        """
        return self.status == UserStatus.INACTIVE

    @property
    def is_deleted(self) -> bool:
        """
        Indicates whether the user was soft-deleted.

        Returns:
            bool: True when the user status is deleted; otherwise, False.
        """
        return self.status == UserStatus.DELETED

    def activate(self):
        """
        Marks the user as active.

        This method only updates the model instance. The caller is responsible
        for committing the database session.
        """
        self.status = UserStatus.ACTIVE
        self.departure_at = None

    def deactivate(self, departure_at=None):
        """
        Marks the user as inactive.

        Args:
            departure_at (datetime, optional): Date when the user left the
                project. When omitted, the current UTC date and time is used.
        """
        self.status = UserStatus.INACTIVE
        self.departure_at = departure_at or datetime.now(timezone.utc)

    def soft_delete(self):
        """
        Marks the user as deleted without removing the database row.

        This keeps historical records and relationships intact while hiding the
        user from flows that only work with active accounts.
        """
        self.status = UserStatus.DELETED

    def to_dict(self, include_address: bool = False) -> dict:
        """
        Converts the user into a safe dictionary for APIs and templates.

        The password hash is never included. CPF and RG are also omitted by
        default because they are sensitive personal identifiers.

        Args:
            include_address (bool): When True, includes the related address data
                if an address is loaded or available.

        Returns:
            dict: Serialized user data.
        """
        data = {
            "id": str(self.id) if self.id else None,
            "code_institutional": self.code_institutional,
            "name": self.name,
            "email": self.email,
            "nationality": self.nationality,
            "marital": self._enum_to_value(self.marital),
            "profession": self.profession,
            "sector": self._enum_to_value(self.sector),
            "position": self._enum_to_value(self.position),
            "profile": self._enum_to_value(self.profile),
            "status": self._enum_to_value(self.status),
            "entry_at": self._datetime_to_iso(self.entry_at),
            "departure_at": self._datetime_to_iso(self.departure_at),
            "created_at": self._datetime_to_iso(self.created_at),
            "update_at": self._datetime_to_iso(self.update_at),
        }

        if include_address and self.address:
            data["address"] = {
                "postal_code": self.address.postal_code,
                "street": self.address.street,
                "number": self.address.number,
                "complement": self.address.complement,
                "neighborhood": self.address.neighborhood,
                "city": self.address.city,
                "state": self.address.state,
                "country": self.address.country,
            }

        return data
    
    @staticmethod
    def validate_cpf(cleaned_cpf: str) -> bool:
        """
        Validates a CPF using its check digits.

        Args:
            cleaned_cpf (str): CPF containing only digits.

        Returns:
            bool: True when the CPF is valid; otherwise, False.
        """
        if not isinstance(cleaned_cpf, str):
            return False

        if not cleaned_cpf.isdigit() or len(cleaned_cpf) != 11 or cleaned_cpf == cleaned_cpf[0] * 11:
            return False
        
        for i in range(9, 11):
            total_sum = 0
            for j in range(0, i):
                total_sum += int(cleaned_cpf[j]) * ((i + 1) - j)
            
            digit = (total_sum * 10) % 11
            if digit == 10:
                digit = 0
                
            if digit != int(cleaned_cpf[i]):
                return False
                
        return True

    @staticmethod
    def email_validate(email):
        """
        Validates and normalizes an email address.

        Args:
            email (str): Email address to validate.

        Returns:
            str | None: Normalized email when valid; otherwise, None.
        """
        try:
            email_check = validate_email(email, check_deliverability=True)
            return email_check.normalized
        except EmailNotValidError:
            return None
        
    @staticmethod
    def rg_validate(rg):
        """
        Normalizes and validates an RG number.

        Args:
            rg (str): RG value submitted by the user.

        Returns:
            str | None: RG containing only digits when valid; otherwise, None.
        """
        rg = ''.join(filter(str.isdigit, rg))
        if len(rg) == 9:
            return rg
        else:
            return None
        
    def _set_default_password(self):
        """
        Creates a default password from the user's first and last name.

        The generated password is normalized with ``unidecode`` and stored as a
        secure hash through ``set_password``.
        """
        name_array = self.name.strip().split(" ")
        if not name_array:
            return
        password_default = unidecode((name_array[0] + name_array[-1]).lower())
        self.set_password(password_default)

    @staticmethod
    def _enum_to_value(enum_item):
        """
        Returns the display value of an enum item.

        Args:
            enum_item (Enum | None): Enum field stored in the model.

        Returns:
            str | None: Enum value when available; otherwise, None.
        """
        return enum_item.value if enum_item else None

    @staticmethod
    def _datetime_to_iso(date_value):
        """
        Converts a datetime value to ISO 8601 format.

        Args:
            date_value (datetime | None): Date value stored in the model.

        Returns:
            str | None: ISO-formatted date string when available; otherwise,
            None.
        """
        return date_value.isoformat() if date_value else None
