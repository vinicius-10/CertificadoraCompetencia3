"""
Expose the application's service functions through a centralized interface.

The exported functions provide authentication, password recovery, email
delivery, and user registration operations.
"""

from app.services.auth_service import authenticate_user, recovery_password_send, recovery_password_register
from app.services.email_service import send_email
from app.services.register_service import register_user


__all__ = [
    "authenticate_user",
    "recovery_password_send, recovery_password_register",
    "register_user",
    "send_email",
]
