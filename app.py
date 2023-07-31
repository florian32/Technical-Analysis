from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException, default_exceptions
from api import(
    service_api,
    user_api
)
from config import config


def make_json_error(ex: Exception) -> jsonify:
    response = jsonify(message=str(ex))
    response.status_code = ex.code if isinstance(ex, HTTPException) else 500
    return response


def create_app():
    app = Flask(__name__)

    with app.app_context():
        app.secret_key = config.SECRET_KEY
        app.config.from_object(config)

    for api in [service_api, user_api]:
        app.register_blueprint(api.blueprint)

    return app
