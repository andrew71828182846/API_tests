import pytest

from src.main.api.models.up_u_balance_request import UpUBalanceRequest
from src.main.api.classes.api_manager import ApiManager


@pytest.mark.api
class TestAccountLimits:
    def test_max_accounts_limit(self, api_manager: ApiManager, create_user_request):

        api_manager.user_steps.create_account(create_user_request)
        api_manager.user_steps.create_account(create_user_request)

        with pytest.raises(Exception, match="maximum number of accounts"):
            api_manager.user_steps.create_account(create_user_request)

    @pytest.mark.parametrize("amount, expected_success", [
        (999, False),  # Ниже минимума
        (1000, True),  # Граница Min
        (5000, True),  # Середина
        (9000, True),  # Граница Max
        (9001, False),  # Выше максимума
    ])
    def test_deposit_limits(
            self,
            api_manager: ApiManager,
            create_user_request,
            up_balance_request: UpUBalanceRequest,
            amount: int,
            expected_success: bool
    ):
        # Arrange: создаем аккаунт (пользователь уже создан фикстурой create_user_request)
        account = api_manager.user_steps.create_account(create_user_request)

        # Модифицируем фикстуру: подменяем amount, сохраняя accountId
        # model_copy — стандарт Pydantic v2 для создания измененной копии
        test_request = up_balance_request.model_copy(update={
            "accountId": account.id,
            "amount": amount
        })

        if expected_success:
            response = api_manager.user_steps.up_balance(
                user_credentials=create_user_request,
                up_balance_request=test_request
            )
            assert response.balance == amount, f"Баланс {response.balance} не совпадает с ожидаемым {amount}"
        else:
            with pytest.raises(Exception):
                api_manager.user_steps.up_balance(
                    user_credentials=create_user_request,
                    up_balance_request=test_request
                )