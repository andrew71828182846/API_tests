from typing import Optional
import allure
import requests

from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.foundation.requesters.crud_requester import CRUDRequester
from src.main.api.models.base_model import BaseModel


class ValidateCrudRequester(HttpRequester):
    def __init__(self, request_spec, endpoint, response_spec):
        super().__init__(request_spec, endpoint, response_spec)
        self.crud_requester = CRUDRequester(
            request_spec=request_spec,
            endpoint=endpoint,
            response_spec=response_spec
        )

    def post(self, model: Optional[BaseModel] = None) -> Optional[BaseModel]:
        response = self.crud_requester.post(model)
        with allure.step(f"POST {Config.fetch("backendurl")}{self.endpoint.value.url} and Validated Model"):
            allure.attach(f"Validated Model response: {self.endpoint.value.response_model.__name__}")



        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())

    def delete(self, user_id: int):
        response = self.crud_requester.delete(user_id)
        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())

    def get(self, item_id: Optional[int] = None) -> Optional[BaseModel]:
        # Формируем URL корректно: с item_id или без
        url = f"{Config.fetch('backendurl')}{self.endpoint.value.url}"
        if item_id is not None:
            url += f"/{item_id}"

        response = self.crud_requester.get(item_id)

        with allure.step(f"GET {url} and Validated Model"):
            allure.attach(f"Validated Model: {self.endpoint.value.response_model.__name__}")

        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())
