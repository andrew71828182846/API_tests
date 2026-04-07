import pytest


@pytest.mark.api
class TestTransferFunds:
    def test_transfer_funds(self, api_manager, transfer_funds_request):
        response = api_manager.user_steps.transfer_funds(
            transfer_funds_request=transfer_funds_request["transfer_request"],
            user_credentials=transfer_funds_request["sender_creds"]
        )

        assert response.fromAccountIdBalance == float(transfer_funds_request["expected_sender_balance"])