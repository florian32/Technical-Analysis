import requests
import os
from flask import Blueprint
from flask import current_app as app
from typing import Dict, Tuple
from flask import request, session
from flask_restful import Api, Resource
from . import QueryParamsParseMixin
from config import config
from utils.stock import Stock

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


@api.resource("/analysis/<symbol>/<image_path>")
class StockAnalysisResource(QueryParamsParseMixin, Resource):
    query_params = {
        "timestamp": lambda req: str(req.args.get("timestamp")),
        "sma": lambda req: str(req.args.get("sma")),
        "res": lambda req: str(req.args.get("res")),
        "formations": lambda req: str(req.args.get("formations")),
    }

    def post(self, symbol) -> Tuple[Dict, int]:
        stock = Stock(symbol, self._request_query_parameters["timestamp"])
        stock.get_min_max()
        stock.find_patterns()
        image_dir, patterns_num = stock.plot_minmax_patterns(sma=self._request_query_parameters["sma"],
                                                             resistance_levels=self._request_query_parameters["res"],
                                                             formations=self._request_query_parameters["formations"])
        return {"image_dir": image_dir, "patterns_num": patterns_num}, 200

    def delete(self, image_path) -> Tuple[Dict, int]:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
            return {"message": "Image deleted successfully."}, 200
        else:
            return {"message": "Image not found or unable to delete."}, 404
