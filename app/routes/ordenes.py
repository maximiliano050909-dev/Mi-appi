# app/routes/ordenes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app import db
from app.models import Orden, DetalleOrden, Producto, Cliente

ordenes_bp = Blueprint('ordenes', __name__, url_prefix='/api/ordenes')


@ordenes_bp.route("/", methods=["POST"])
@jwt_required()
def procesar_orden():
    """
    Procesa una nueva orden de compra.
    Requiere autenticacion JWT.

    Body esperado:
    {
        "cliente_id": 1,
        "productos": [
            {"producto_id": 5, "cantidad": 2},
            {"producto_id": 12, "cantidad": 1}
        ]
    }
    """

    datos = request.get_json()
    total = 0
    detalles = []
    errores = []

    # Validar cada producto antes de crear la orden
    for item in datos["productos"]:
        producto = Producto.query.get(item["producto_id"])

        if not producto:
            errores.append(f"Producto ID {item['producto_id']} no existe")
            continue

        if producto.stock < item["cantidad"]:
            errores.append(
                f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}"
            )
            continue

        subtotal = float(producto.precio) * item["cantidad"]
        total += subtotal

        detalles.append({
            "producto": producto,
            "cantidad": item["cantidad"],
            "precio_unitario": float(producto.precio)
        })

    # Si hay errores, no procesar la orden
    if errores:
        return jsonify({
            "error": "No se pudo procesar",
            "detalles": errores
        }), 400

    # Crear la orden (todo en una sola transaccion)
    try:
        orden = Orden(cliente_id=datos["cliente_id"], total=total)
        db.session.add(orden)

        # Obtener ID sin hacer commit
        db.session.flush()

        for d in detalles:
            # Crear detalle de orden
            detalle = DetalleOrden(
                orden_id=orden.id,
                producto_id=d["producto"].id,
                cantidad=d["cantidad"],
                precio_unitario=d["precio_unitario"]
            )
            db.session.add(detalle)

            # Reducir stock
            d["producto"].stock -= d["cantidad"]

        # Confirmar cambios
        db.session.commit()

        return jsonify({
            "mensaje": "Orden procesada exitosamente",
            "orden_id": orden.id,
            "total": total,
            "productos_comprados": len(detalles)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Error interno",
            "detalle": str(e)
        }), 500