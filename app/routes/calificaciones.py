# app/routes/calificaciones.py
from flask import Blueprint, jsonify, request
from app import db
from app.models.calificacion import Calificacion
from app.models.estudiante import Estudiante
from sqlalchemy import func

cal_bp = Blueprint('calificaciones', __name__, url_prefix='/api')

@cal_bp.route("/estudiantes/<int:id>/kardex", methods=["GET"])
def obtener_kardex(id):
    """
    Obtiene el kardex completo de un estudiante.
    Incluye todas sus materias, calificaciones y estadisticas.
    """
    estudiante = Estudiante.query.get_or_404(id)
    calificaciones = Calificacion.query.filter_by(estudiante_id=id).all()

    if not calificaciones:
        return jsonify({
            "estudiante": estudiante.to_dict(),
            "mensaje": "Sin calificaciones registradas",
            "calificaciones": []
        }), 200

    # Calcular estadisticas
    valores = [float(c.calificacion) for c in calificaciones]
    promedio = sum(valores) / len(valores)
    materias_aprobadas = sum(1 for v in valores if v >= 60)

    return jsonify({
        "estudiante": estudiante.to_dict(),
        "estadisticas": {
            "promedio_general": round(promedio, 2),
            "total_materias": len(calificaciones),
            "materias_aprobadas": materias_aprobadas,
            "materias_reprobadas": len(calificaciones) - materias_aprobadas,
            "calificacion_maxima": max(valores),
            "calificacion_minima": min(valores),
            "estatus": "Regular" if promedio >= 70 else "En riesgo"
        },
        "calificaciones": [c.to_dict() for c in calificaciones]
    }), 200


@cal_bp.route("/calificaciones/", methods=["POST"])
def registrar_calificacion():
    """Registra una nueva calificacion para un estudiante."""
    datos = request.get_json()

    # Validar rango de calificacion (0-100)
    cal = datos.get("calificacion", 0)
    if not 0 <= float(cal) <= 100:
        return jsonify({"error": "La calificacion debe estar entre 0 y 100"}), 400

    nueva = Calificacion(
        estudiante_id=datos["estudiante_id"],
        materia_id=datos["materia_id"],
        calificacion=cal,
        periodo=datos.get("periodo", "2024-1")
    )

    db.session.add(nueva)
    db.session.commit()

    return jsonify(nueva.to_dict()), 201