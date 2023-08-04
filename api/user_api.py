import requests
from flask import Blueprint
from flask import current_app as app
from typing import Dict, Tuple
from flask import request, session
from flask_restful import Api, Resource

from config import config

blueprint = Blueprint("api/users", __name__, url_prefix="/api")
api = Api(blueprint)