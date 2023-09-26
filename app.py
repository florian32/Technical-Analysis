from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException, default_exceptions
from sqlalchemy.exc import OperationalError
from api import(
    service_api,
    user_api
)
from db import db
from config import config


def make_json_error(ex: Exception) -> jsonify:
    response = jsonify(message=str(ex))
    response.status_code = ex.code if isinstance(ex, HTTPException) else 500
    return response


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the SQLAlchemy extension
    db.init_app(app)

    with app.app_context():
        app.secret_key = config.SECRET_KEY
        app.config.from_object(config)
        try:
            db.create_all()
        except OperationalError as e:
            print(f"Error {e}")
    for api in [service_api, user_api]:
        app.register_blueprint(api.blueprint)

    return app
