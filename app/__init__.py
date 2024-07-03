from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# Initialize the extensions
db = SQLAlchemy()
api = Api()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Load the configuration from config.py
    app.config.from_object('app.config.Config')

    # Initialize the extensions with the app
    db.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    return app
