import pytest


@pytest.mark.api
class TestGetCredit:
    def test_get_credit(self, api_manager, credit_user_credentials, get_credit_request):
        response = api_manager.user_steps.get_credit(
            user_request=credit_user_credentials,
            get_credit_request=get_credit_request
        )
        assert response.creditId is not None


