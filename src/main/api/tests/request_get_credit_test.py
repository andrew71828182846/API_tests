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
    def test_get_credit(self):
        create_user_request = CreateUserRequest(username="Max345", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max345", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        account_id1 = response.id

        get_credit_request = GetCreditRequest(accountId=account_id1, amount=5000, termMonths=12)
        credit_response = GetCreditRequester(
            request_spec=RequestSpecs.auth_headers(username="Max345", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post(get_credit_request)


        assert credit_response.termMonths == get_credit_request.termMonths
