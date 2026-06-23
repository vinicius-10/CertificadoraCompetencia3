"""
Manages the generation, storage, validation, and lifecycle of user validation tokens.
"""
from datetime import datetime, timedelta, timezone
import secrets
import uuid

from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from flask import current_app

from app.models.db_instance import db
        
class PasswordRecoveryToken(db.Model):
    __tablename__ = 'password_recovery_tokens'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    
    user = relationship("User", back_populates="recovery_tokens")

    def __init__(self, **kwargs):
        """
        Initializes a password recovery token.

        Automatically generates:
            id
            is_used
            created_at
            secure token
            expiration timestamp
        Automatically generates a secure token and expiration timestamp
        when these values are not already set, ensuring that newly created
        instances are ready for use in the password recovery workflow.

        Args:
            **kwargs: Model attributes passed to the parent constructor.
        Return:
            PasswordRecoveryToken: Object
        """
        super(PasswordRecoveryToken, self).__init__(**kwargs)
        
        if self.token is None:
            self.token = secrets.token_urlsafe(32)
            
        if self.expires_at is None:
            hours_expiration = current_app.config['TOKEN_EXPIRATION_TIME']
            self.expires_at = datetime.now(timezone.utc) + timedelta(hours=hours_expiration)
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the password recovery token instance.

        The representation includes key attributes that are useful for
        debugging and logging purposes.

        Returns:
            str: A human-readable representation of the token instance.
        """
        return f"<PasswordRecoveryToken user_id={self.user_id} created_at={self.created_at} expires_at={self.expires_at} is_used={self.is_used}>"

    def __str__(self) -> str:
        """
        Returns a user-friendly description of the password recovery token.

        Returns:
            str: A summary containing the associated user, creation date,
                expiration date, and usage status.
        """
        return (
            f"Password recovery token for user {self.user_id} "
            f"(created: {self.created_at}, "
            f"expires: {self.expires_at}, "
            f"used: {self.is_used})"
        )
    
    def set_token(self) -> str:
        """
        Generates and assigns a new secure validation token.

        The token can be used for account verification, password recovery,
        or other user validation processes.

        Returns:
            str: The generated validation token.
        """
        self.token = secrets.token_urlsafe(32)
        return self.token

    def set_expiration_date(self) -> datetime:
        """
        Calculates and sets the token expiration date based on the application configuration.

        The expiration timestamp is determined by adding the configured
        token lifetime to the current UTC date and time.

        Returns:
            datetime: The calculated expiration timestamp in UTC.
        """
        hours_expiration = current_app.config['TOKEN_EXPIRATION_TIME']
        self.expires_at = (datetime.now(timezone.utc) + timedelta(hours=hours_expiration))
        return  self.expires_at
    
    def is_valid(self) -> bool:
        """
        Checks whether the token is currently valid.

        A token is considered valid if it has not been used and its
        expiration timestamp has not been reached.

        Returns:
            bool: True if the token is valid; otherwise, False.
        """
        current_time = datetime.now(timezone.utc)
        return not self.is_used and current_time < self.expires_at
    
