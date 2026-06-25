import os
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from app.models import db, User
from app.seed import seed_data
from app.config import Config
from flask_mailman  import Mail

migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    mail = Mail(app)
    
    _configure_login_manager(app)

    _register_blueprints(app)

    @app.cli.command("seed-db")
    def seed_db_command():
        seed_data()

    return app

def _configure_login_manager(app):
    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

def _register_blueprints(app):
    
    import app.routes as rt

    app.register_blueprint(rt.main_bp)
    app.register_blueprint(rt.api_bp, url_prefix="/api")
    
    
    if app.config.get('ENV') == 'development' or os.environ.get('FLASK_ENV') == 'development':
        app.register_blueprint(rt.test_bp, url_prefix="/test")