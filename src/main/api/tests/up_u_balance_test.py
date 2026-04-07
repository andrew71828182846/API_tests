import pytest


@pytest.mark.api
class Test_up_u_balance:
    def test_up_u_balance(self, api_manager, create_user_request, up_balance_request):
        response = api_manager.user_steps.up_balance(up_balance_request=up_balance_request, user_credentials=create_user_request)

        assert response.balance == float(up_balance_request.amount)







