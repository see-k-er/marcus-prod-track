# app/__init__.py

from flask import Flask

from dotenv import load_dotenv
import os
from app.routes.worker import worker_bp
from app.routes.admin import admin_bp
from app.routes.management import management_bp
from app.extensions import db, migrate, login_manager


# Load environment variables from .env
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # 👇 Move this here to avoid circular import
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = 'auth.login'

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.worker import worker_bp
    from app.routes.admin import admin_bp
    from app.routes.management import management_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(worker_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(management_bp)

    return app


#app.config.from_object('config.Config')


