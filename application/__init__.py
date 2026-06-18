from flask import Flask
from flask import render_template
from flask_migrate import Migrate
from seed import seed_data
from flask_login import LoginManager
from models import db, User
import os
from datetime import timedelta

from models import db



def create_app(test_config=None):
    
    app = Flask(__name__)
    if test_config:
        app.config.update(test_config)
    return app

def _register_blueprints(app):
    from main_routes import main_bp
    from test_routes import test_bp
    from api_routes import api_bp 
    app.register_blueprint(main_bp)
    app.register_blueprint(test_bp, url_prefix="/test")
    app.register_blueprint(api_bp, url_prefix="/api")