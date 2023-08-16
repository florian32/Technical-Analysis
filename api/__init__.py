from typing import Dict
from flask import request


class QueryParamsParseMixin:
    query_params = {}

    @property
    def _request_query_parameters(self) -> Dict:
        result = {}
        for key, func in self.query_params.items():
            val = func(request)
            if val is not None:
                result[key] = val
        return result
