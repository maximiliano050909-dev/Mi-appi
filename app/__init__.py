# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import DevelopmentConfig

# Crear la instancia de SQLAlchemy (el ORM)
# ORM = Object Relational Mapper: convierte tablas en clases Python
db = SQLAlchemy()

def create_app(config=DevelopmentConfig):
    """
    Patrón Application Factory: crea y configura la app Flask.
    Esto permite crear múltiples instancias con diferentes configuraciones.
    """
    app = Flask(__name__)

    # Cargar configuración
    app.config.from_object(config)

    # Inicializar extensiones con la app
    db.init_app(app)
    CORS(app)  # Permite peticiones desde otros dominios (ej. React)

    # Registrar rutas (blueprints)
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app