# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger
from .config import DevelopmentConfig

# instancia global de SQLAlchemy
db = SQLAlchemy()


def create_app(config=DevelopmentConfig):

    app = Flask(__name__)

    # cargar configuracion
    app.config.from_object(config)

    # inicializar extensiones
    db.init_app(app)
    CORS(app)

    # -----------------------
    # Configuracion Swagger
    # -----------------------

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json"
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/"
    }

    swagger_template = {
        "info": {
            "title": "API Escolar - ITIC",
            "version": "1.0.0",
            "description": "API REST para gestion escolar"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header"
            }
        }
    }

    Swagger(app, config=swagger_config, template=swagger_template)

    # -----------------------
    # Registrar Blueprints
    # -----------------------

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app