"""
Expose the application's database instance, models, and enumerations.

Importing the models in this module ensures that SQLAlchemy can discover their
table mappings and provides a centralized interface for accessing persistence
entities throughout the application.
"""

#docker-compose exec web flask db migrate -m "descricao"
#docker-compose exec web flask db upgrade


from app.models.db_instance import db

from app.models.user import User
from app.models.address import Address
from app.models.status_history import StatusHistory
from app.models.access_log import AccessLog
from app.models.password_recovery import PasswordRecoveryToken
from app.models.user_block import UserBlock
from app.models.enums import UserProfile, UserStatus, UserMarital, UserSector, UserPosition

__all__ = [
    'db', 
    'User', 
    'Address', 
    'StatusHistory', 
    'AccessLog', 
    'PasswordRecoveryToken', 
    'UserBlock',
    'UserProfile',
    'UserStatus',
    'UserMarital',
    'UserSector',
    'UserPosition'
]
