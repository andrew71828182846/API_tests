import requests
from requests import Response

from src.main.api.request.requester import Requester


class DeleteAllRequester(Requester):
    def post(self) -> Response:
        url=f"{self.base_url}/admin/users"
        response=requests.delete(
            url=url,
            headers=self.headers
        )
        self.response_spec(response)
        return response