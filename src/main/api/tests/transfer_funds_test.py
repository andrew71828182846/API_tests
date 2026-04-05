import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_funds_request import TransferFundsRequest
from src.main.api.models.up_u_balance_request import UpUBalanceRequest
from src.main.api.request.create_account_requester import CreateAccountRequester
from src.main.api.request.create_user_requester import CreateUserRequester
from src.main.api.request.transfer_funds_requester import TransferFundsRequester
from src.main.api.request.up_balance_requester import UpBalanceRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestTransferFunds:
    def test_transfer_funds(self):
        create_user_request1 = CreateUserRequest(username="Max3", password="Pas!sw0rd", role="ROLE_USER")


        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request1)

        response1 = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max3", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        account_id1 = response1.id


        up_u_balance_request = UpUBalanceRequest(accountId=account_id1, amount=1100)
        UpBalanceRequester(
            request_spec=RequestSpecs.auth_headers(username="Max3", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(up_u_balance_request)


        create_user_request2 = CreateUserRequest(username="Max5", password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request2)

        response2 = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max5", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        account_id2 = response2.id


        transfer_funds_request = TransferFundsRequest(fromAccountId=account_id1, toAccountId=account_id2, amount=500.75)
        TransferFundsRequester(
            request_spec=RequestSpecs.auth_headers(username="Max3", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(transfer_funds_request)

