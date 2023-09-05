import requests
from flask import Blueprint
from flask import current_app as app
from typing import Dict, Tuple
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, session
from flask_restful import Api, Resource
from . import QueryParamsParseMixin
from db import User, Search, db
from config import config

blueprint = Blueprint("api/users", __name__, url_prefix="/api/users")
api = Api(blueprint)


@api.resource("/administrate")
class UserResource(QueryParamsParseMixin, Resource):
    query_params = {
        "email": lambda req: str(req.args.get("email")),
        "password": lambda req: str(req.args.get("password")),
        "name": lambda req: str(req.args.get("name")),
    }

    def post(self) -> Tuple[Dict, int]:
        hashed_password = generate_password_hash(
            self._request_query_parameters["password"],
            method=config.HASH_METHOD,
            salt_length=config.SALT_LENGTH
        )
        new_user = User(
            email=self._request_query_parameters["email"],
            password=hashed_password,
            name=self._request_query_parameters["name"],
        )
        db.session.add(new_user)
        db.session.commit()
        return {"Success": "letsgo"}, 200

