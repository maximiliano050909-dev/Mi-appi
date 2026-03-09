# app/models/materia.py
from app import db

class Materia(db.Model):
    __tablename__ = 'materias'

    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(10), unique=True, nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    creditos = db.Column(db.Integer, nullable=False)
    docente = db.Column(db.String(100))

    # Relacion: una materia tiene muchas calificaciones
    calificaciones = db.relationship('Calificacion', back_populates='materia')

    def to_dict(self):
        return {
            "id": self.id,
            "clave": self.clave,
            "nombre": self.nombre,
            "creditos": self.creditos
        }