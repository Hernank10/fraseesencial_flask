from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión'
    
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.examples import examples_bp
    from app.routes.practice import practice_bp
    from app.routes.flashcards import flashcards_bp
    from app.routes.writing import writing_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(examples_bp, url_prefix='/examples')
    app.register_blueprint(practice_bp, url_prefix='/practice')
    app.register_blueprint(flashcards_bp, url_prefix='/flashcards')
    app.register_blueprint(writing_bp, url_prefix='/writing')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
