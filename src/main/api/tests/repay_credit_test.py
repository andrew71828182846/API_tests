from http.client import responses

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.get_credit_request import GetCreditRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.request.create_account_requester import CreateAccountRequester
from src.main.api.request.create_user_requester import CreateUserRequester
from src.main.api.request.get_credit_requester import GetCreditRequester
from src.main.api.request.repay_credit_requester import RepayCreditRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestRepayCredit:
    def test_repay_credit(self, api_manager, repay_credit_request: RepayCreditRequest, credit_user_credentials):
        response = api_manager.user_steps.repay_credit(credit_user_credentials, repay_credit_request)

        assert response.amountDeposited == repay_credit_request.amount