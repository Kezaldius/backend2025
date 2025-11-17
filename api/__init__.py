# api/__init__.py
from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from .models import db

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    api = Api(app)
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "Token expired", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({"message": "Invalid token.", "error": "invalid_token"}),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({
                "description": "No token provided.",
                "error": "authorization_required",
            }),
            401,
        )

    db.init_app(app)
    migrate = Migrate(app, db)

    from . import views
    api.register_blueprint(views.blp)

    return app