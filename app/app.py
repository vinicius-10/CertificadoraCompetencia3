
from flask import Flask
from flask import render_template
from flask_migrate import Migrate
from seed import seed_data
from flask_login import LoginManager
from models import db, User
import os
from datetime import timedelta

from models import db

app = Flask(__name__)

env = os.environ
app.config['SQLALCHEMY_DATABASE_URI'] = env.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SESSION_COOKIE_DURATION'] = timedelta(hours=8)
app.config['SESSION_COOKIE_LIFETIME'] = timedelta(hours=8)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False if (os.environ.get('FLASK_ENV') == 'development') else True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

db.init_app(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


from main_routes import main_bp
from test_routes import test_bp
app.register_blueprint(main_bp)
app.register_blueprint(test_bp, url_prefix="/test")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

@app.cli.command("seed-db")
def seed_db_command():
    seed_data()
    
