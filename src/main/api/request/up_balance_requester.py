import requests
from src.main.api.models.up_u_balance_request import UpUBalanceRequest
from src.main.api.models.up_u_balance_response import UpUBalanceResponse
from src.main.api.request.requester import Requester


class UpBalanceRequester(Requester):
    def post(self, up_u_balance_request: UpUBalanceRequest) -> UpUBalanceResponse:
        url=f"{self.base_url}/account/deposit"
        response = requests.post(
            url=url,
            json=up_u_balance_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        return UpUBalanceResponse(**response.json())