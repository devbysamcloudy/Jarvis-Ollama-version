from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jarvis.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "jarvis-secret-key-change-in-production"

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from routes.auth import auth_bp
    from routes.history import history_bp
    from routes.preferences import prefs_bp
    from routes.commands import commands_bp
    from routes.weather import weather_bp
    from routes.notifications import notifications_bp
    
    app.register_blueprint(notifications_bp, url_prefix="/api/notifications")
    app.register_blueprint(weather_bp, url_prefix="/api/weather")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(history_bp, url_prefix="/api/history")
    app.register_blueprint(prefs_bp, url_prefix="/api/preferences")
    app.register_blueprint(commands_bp, url_prefix="/api/commands")
    
    with app.app_context():
        db.create_all()

    return app