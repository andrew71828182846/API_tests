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
    def test_transfer_funds(self, api_manager, transfer_test_setup):
        response = api_manager.user_steps.transfer_funds(
            transfer_funds_request=transfer_test_setup["transfer_request"],
            user_credentials=transfer_test_setup["sender_creds"]
        )

        assert response.fromAccountIdBalance == transfer_test_setup["expected_sender_balance"]
