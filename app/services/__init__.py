"""
Expose the application's service functions through a centralized interface.

The exported functions provide authentication, password recovery, email
delivery, and user registration operations.
"""

from app.services.adm_service import generate_users_report_csv, generate_users_report_pdf, search_users
from app.services.auth_service import authenticate_user, recovery_password_send, recovery_password_register
from app.services.email_service import send_email
from app.services.register_service import register_user
from app.services.update_service import update_user_from_user, update_user_from_admin, delete_user_amd


__all__ = [
    "authenticate_user",
    "generate_users_report_csv",
    "generate_users_report_pdf",
    "recovery_password_send",
    "recovery_password_register",
    "register_user",
    "search_users",
    "send_email",
    "update_user_from_user",
    "update_user_from_admin",
    "delete_user_amd",
]
