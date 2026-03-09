# app/models/calificacion.py
from app import db
from datetime import datetime

class Calificacion(db.Model):
    __tablename__ = 'calificaciones'

    id = db.Column(db.Integer, primary_key=True)

    # Claves foraneas - conectan con otras tablas
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)

    calificacion = db.Column(db.Numeric(5, 2), nullable=False)  # Ej: 95.50
    periodo = db.Column(db.String(20))  # Ej: '2024-1'
    fecha_evaluacion = db.Column(db.Date, default=datetime.utcnow)

    # Relaciones bidireccionales
    estudiante = db.relationship('Estudiante', back_populates='calificaciones')
    materia = db.relationship('Materia', back_populates='calificaciones')

    def to_dict(self):
        return {
            "id": self.id,
            "estudiante": f"{self.estudiante.nombre} {self.estudiante.apellido}",
            "materia": self.materia.nombre,
            "calificacion": float(self.calificacion),
            "aprobado": float(self.calificacion) >= 60,
            "periodo": self.periodo
        }