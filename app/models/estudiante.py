# app/models/estudiante.py
from app import db
from datetime import datetime

class Estudiante(db.Model):
    """
    Modelo que representa la tabla "estudiantes" en PostgreSQL.
    SQLAlchemy creará automáticamente la tabla con estos campos.
    """

    # Nombre de la tabla en la base de datos
    __tablename__ = "estudiantes"

    # Columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)  # PK autoincremental
    matricula = db.Column(db.String(10), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    carrera = db.Column(db.String(100), nullable=False)
    semestre = db.Column(db.Integer, nullable=False, default=1)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)

    def to_dict(self):
        """Convierte el objeto a un diccionario (para enviarlo como JSON)."""
        return {
            "id": self.id,
            "matricula": self.matricula,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "nombre_completo": f"{self.nombre} {self.apellido}",
            "email": self.email,
            "carrera": self.carrera,
            "semestre": self.semestre,
            "fecha_registro": self.fecha_registro.isoformat(),
            "activo": self.activo
        }

    def __repr__(self):
        """Representación en texto del objeto (para depuración)."""
        return f"<Estudiante {self.matricula}: {self.nombre} {self.apellido}>"