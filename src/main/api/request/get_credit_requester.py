import requests
from requests import Response
from src.main.api.models.get_credit_request import GetCreditRequest
from src.main.api.models.get_credit_response import GetCreditResponse
from src.main.api.request.requester import Requester


class GetCreditRequester(Requester):
    def post(self, get_credit_request: GetCreditRequest) -> GetCreditResponse | Response:
        url=f"{self.base_url}/credit/request"
        response=requests.post(
            url=url,
            json=get_credit_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        return GetCreditResponse(**response.json())