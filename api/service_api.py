import requests
from flask import Blueprint
from flask import current_app as app
from typing import Dict, Tuple
from flask import request, session
from flask_restful import Api, Resource

from config import config

blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint)


@api.resource("/news")
class NewsListResource(Resource):
    query_params = {
        "published_after": lambda req: int(req.args.get("published_after", 3)),
        "entity_types": lambda req: str(req.args.get("entity_types")),
        "industries": lambda req: str(req.args.get("industries")),
        "symbols": lambda req: str(req.args.get("symbols")),
        "limit": lambda req: int(req.args.get("limit", 3)),
        "api_token": config.MARKETAUX_TOKEN
    }

    def get(self) -> Tuple[Dict, int]:
        response = requests.get(config.MARKETAUX_ENDPOINT, headers=self.query_params)
        return response

