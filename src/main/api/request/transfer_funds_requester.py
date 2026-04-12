import requests
from requests import Response
from src.main.api.models.transfer_funds_request import TransferFundsRequest
from src.main.api.models.transfer_funds_response import TransferFundsResponse
from src.main.api.request.requester import Requester


class TransferFundsRequester(Requester):
    def post(self, transfer_funds_request: TransferFundsRequest) -> TransferFundsResponse | Response:
        url=f"{self.base_url}/account/transfer"
        response=requests.post(
            url=url,
            json=transfer_funds_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        return TransferFundsResponse(**response.json())