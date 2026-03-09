# run.py - Ejecutar con: python run.py
from app import create_app, db

app = create_app()

if __name__ == "__main__":
    # with app.app_context() crea el contexto de aplicación necesario
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
        print("Tablas creadas correctamente")

    print("Servidor iniciado en http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)