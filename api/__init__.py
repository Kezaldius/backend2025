# api/__init__.py
from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from .models import db

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    api = Api(app)
    jwt = JWTManager(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    from . import views
    api.register_blueprint(views.blp)

    return app