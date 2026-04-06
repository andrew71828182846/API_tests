import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.get_credit_request import GetCreditRequest
from src.main.api.request.create_account_requester import CreateAccountRequester
from src.main.api.request.create_user_requester import CreateUserRequester
from src.main.api.request.get_credit_requester import GetCreditRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs

@pytest.mark.api
class TestGetCredit:
    def test_get_credit(self, api_manager, credit_user_credentials, get_credit_request):
        response = api_manager.user_steps.get_credit(
            user_request=credit_user_credentials,
            get_credit_request=get_credit_request
        )
        assert response.creditId is not None


