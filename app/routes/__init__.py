# app/routes/__init__.py
from flask import Blueprint, jsonify
from datetime import datetime

# Blueprint: es como un modulo de rutas que se puede registrar en la app
main_bp = Blueprint('main', __name__)

@main_bp.route("/", methods=["GET"])
def index():
    """Ruta raiz - bienvenida."""
    return jsonify({
        "mensaje": "Bienvenido a mi primera API con Flask!",
        "version": "1.0.0",
        "tecnologias": ["Python", "Flask", "PostgreSQL"]
    })

@main_bp.route("/health", methods=["GET"])
def health_check():
    """
    Ruta de verificacion de salud de la API.
    Los servicios en produccion usan esto para saber si la app esta viva.
    """
    return jsonify({
        "estado": "OK",
        "timestamp": datetime.now().isoformat(),
        "base_de_datos": "Conectada"
    }), 200