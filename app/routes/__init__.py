"""
Expose the application's route blueprints through a centralized interface.

The exported blueprints include the main application routes, development and
testing routes, and API endpoints.
"""

from app.routes.main_routes import main_bp
from app.routes.test_routes import test_bp

from app.routes.api import api_bp

__all__ = [
    'main_bp',
    'test_bp',
    'api_bp'
]
