from flask import Flask
from marshmallow import ValidationError
from http.client import HTTPException

from .config import Config
from .extensions import db, ma, migrate, jwt
from .routes.messages import messages_bp
from .routes.users import users_bp
from .routes.services import services_bp
from .routes.orders import orders_bp


def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.json.ensure_ascii = False

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)

    from .models import message, user, service  # noqa: F401

    app.register_blueprint(messages_bp, url_prefix="/messages")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(services_bp, url_prefix="/services")
    app.register_blueprint(orders_bp, url_prefix="/orders")

    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        return {"success": False, "errors": err.messages}, 400

    @app.errorhandler(404)
    def handle_404(err):
        return {"success": False, "message": "Recurso nao encontrado"}, 404

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        # Passa o código de erro correto se for um HTTPException
        if isinstance(e, HTTPException):
            return e
        # Se for uma exceção inesperada (ex: bug no Python), retorna 500
        return {"success": False, "message": "Erro interno do servidor"}, 500
    
    return app
