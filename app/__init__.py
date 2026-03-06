from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import DevelopmentConfig

db = SQLAlchemy()

def create_app(config=DevelopmentConfig):

    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    CORS(app)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app