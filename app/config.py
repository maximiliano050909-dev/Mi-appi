# app/config.py
import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

class Config:
    """Clase de configuración base para Flask."""

    # Clave secreta para firmar sesiones y tokens
    SECRET_KEY = os.getenv("SECRET_KEY", "clave-por-defecto-insegura")

    # URL de conexión a la base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    # Desactiva el seguimiento de modificaciones (consume memoria)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mostrar las consultas SQL en consola (útil para depurar)
SQLALCHEMY_ECHO = True

class DevelopmentConfig(Config):
    """Configuración para desarrollo local."""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración para producción (servidor real)."""
    DEBUG = False
    SQLALCHEMY_ECHO = False # No mostrar SQL en producción