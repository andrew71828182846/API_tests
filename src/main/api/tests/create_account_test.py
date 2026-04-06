import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.request.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.request.create_account_requester import CreateAccountRequester


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, api_manager, create_user_request):
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0
