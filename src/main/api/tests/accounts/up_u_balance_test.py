import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.up_u_balance_request import UpUBalanceRequest
from src.main.api.db.models.repay_credit_table import Transaction


@pytest.mark.api
class TestUpUBalance:
    def test_up_u_balance(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            up_balance_request: UpUBalanceRequest,
            db_session: Session
    ):

        response = api_manager.user_steps.up_balance(
            up_balance_request=up_balance_request,
            user_credentials=create_user_request
        )

        assert response.balance == up_balance_request.amount, \
            f"Баланс {response.balance} не совпадает с ожидаемым {up_balance_request.amount}"

        transactions = db_session.query(Transaction).filter(
            Transaction.to_account_id == up_balance_request.accountId,
            Transaction.transaction_type == "deposit",
            Transaction.amount == up_balance_request.amount
        ).all()

        assert len(transactions) == 1, \
            f"Ожидалась 1 транзакция пополнения, найдено: {len(transactions)}"

        transaction = transactions[0]
        assert transaction.to_account_id == up_balance_request.accountId, \
            f"Неверный ID счёта: {transaction.to_account_id}"
        assert transaction.transaction_type == "deposit", \
            f"Неверный тип транзакции: {transaction.transaction_type}"

    def test_get_transactions_after_deposit(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            up_balance_request: UpUBalanceRequest
    ):

        account_id = up_balance_request.accountId
        expected_amount = up_balance_request.amount

        api_manager.user_steps.up_balance(
            user_credentials=create_user_request,
            up_balance_request=up_balance_request
        )

        response = api_manager.user_steps.get_transactions(
            user_credentials=create_user_request,
            account_id=account_id
        )

        assert response.id == account_id, f"Неверный ID аккаунта: {response.id}"
        assert response.balance == pytest.approx(expected_amount, rel=1e-5), \
            f"Баланс {response.balance} не совпадает с ожидаемым {expected_amount}"
        assert len(response.transactions) == 1, "Ожидается ровно одна транзакция"
        transaction = response.transactions[0]
        assert transaction.amount == pytest.approx(expected_amount, rel=1e-5), \
            f"Сумма транзакции {transaction.amount} не совпадает с {expected_amount}"