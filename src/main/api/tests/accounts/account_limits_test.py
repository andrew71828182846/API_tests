import pytest
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.up_u_balance_request import UpUBalanceRequest
from src.main.api.classes.api_manager import ApiManager


@pytest.mark.api
class TestAccountLimits:
    def test_max_accounts_limit(self, api_manager: ApiManager, create_user_request: CreateUserRequest):
        api_manager.user_steps.create_account(create_user_request)
        api_manager.user_steps.create_account(create_user_request)

        error_payload = api_manager.user_steps.create_account(create_user_request, response_spec=ResponseSpecs.request_conflict())

        assert "User already has maximum number of accounts" in error_payload.get("error", ""), \
            f"Неверное сообщение ошибки: {error_payload}"

    @pytest.mark.parametrize("amount", [1000, 5000, 9000])
    def test_deposit_limits_success(self, api_manager: ApiManager, create_user_request: CreateUserRequest, amount: int):
        account = api_manager.user_steps.create_account(create_user_request)
        test_request = UpUBalanceRequest(accountId=account.id, amount=amount)

        response = api_manager.user_steps.up_balance(
            user_credentials=create_user_request,
            up_balance_request=test_request
        )

        assert response.balance == amount, \
            f"Баланс {response.balance} не совпадает с ожидаемым {amount}"

    @pytest.mark.parametrize("amount", [999, 9001])
    def test_deposit_limits_failure(self, api_manager: ApiManager, create_user_request: CreateUserRequest, amount: int):
        account = api_manager.user_steps.create_account(create_user_request)
        test_request = UpUBalanceRequest(accountId=account.id, amount=amount)

        error_payload = api_manager.user_steps.up_balance(
            user_credentials=create_user_request,
            up_balance_request=test_request,
            response_spec=ResponseSpecs.request_bad()
        )

        assert "error" in error_payload, \
            f"Ожидалась ошибка при amount={amount}, получен ответ: {error_payload}"