"""
Expose the application's service functions through a centralized interface.

The exported functions provide authentication, password recovery, email
delivery, and user registration operations.
"""

from app.services.auth_service import authenticate_user, recovery_password
from app.services.email_service import send_email
from app.services.register_service import register_user


__all__ = [
    "authenticate_user",
    "recovery_password",
    "register_user",
    "send_email",
]
