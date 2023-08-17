import requests
from flask import Blueprint
from flask import current_app as app
from typing import Dict, Tuple
from flask import request, session
from flask_restful import Api, Resource
from . import QueryParamsParseMixin
from config import config

blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint)


@api.resource("/news")
class NewsListResource(QueryParamsParseMixin, Resource):
    query_params = {
        "symbols": lambda req: str(req.args.get("symbols")),
        "limit": lambda req: int(req.args.get("limit", 3)),
    }

    def get(self) -> Tuple[Dict, int]:
        response = requests.get(config.MARKETAUX_ENDPOINT,
                                params={"symbols": self._request_query_parameters["symbols"],
                                        "limit": self._request_query_parameters["limit"],
                                        "api_token": config.MARKETAUX_TOKEN}).json()

        return response, 200


@api.resource("/analysis/<symbol>")
class StockAnalysisResource(QueryParamsParseMixin, Resource):
    query_params = {
        "timestamp": lambda req: str(req.args.get("timestamp")),
        "analysis_types": lambda req: str(req.args.get("analysis_types", 3)).split(','),
    }

    def post(self) -> Tuple[Dict, int]:
        pass
