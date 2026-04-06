import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.up_u_balance_request import UpUBalanceRequest
from src.main.api.request.create_account_requester import CreateAccountRequester
from src.main.api.request.create_user_requester import CreateUserRequester
from src.main.api.request.up_balance_requester import UpBalanceRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class Test_up_u_balance:
    def test_up_u_balance(self, api_manager, create_user_request, up_balance_request):
        response = api_manager.user_steps.up_balance(up_balance_request=up_balance_request, user_credentials=create_user_request)

        assert response.balance == 1000







