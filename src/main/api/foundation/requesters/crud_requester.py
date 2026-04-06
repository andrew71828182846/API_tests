import requests
from requests import Response
from typing import Optional
from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.models.base_model import BaseModel


class CRUDRequester(HttpRequester):
    def post(self, model: Optional[BaseModel]) -> Response:
        body = model.model_dump() if model is not None else ""

        response = requests.post(
            url=f"{Config.fetch("backendurl")}{self.endpoint.value.url}",
            headers=self.request_spec,
            json=body
        )
        self.response_spec(response)
        return response


    def delete(self, user_id: int) -> Response:
        response = requests.delete(
            url=f"{Config.fetch("backendurl")}{self.endpoint.value.url}/{user_id}",
            headers=self.request_spec
        )
        self.response_spec(response)
        return response

    def delete_all(self) -> Response:
        response = requests.delete(
            url=f"{Config.fetch("backendurl")}{self.endpoint.value.url}",
            headers=self.request_spec
        )
        self.response_spec(response)
        return response