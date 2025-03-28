from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
import os

db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()


def create_app():
    app = Flask(__name__)

    # Configuración básica
    app.config.from_pyfile('config.py')

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    # Registrar blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Crear tablas de la base de datos
    with app.app_context():
        db.create_all()

    return app