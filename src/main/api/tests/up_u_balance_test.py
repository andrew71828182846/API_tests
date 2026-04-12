import pytest

from src.main.api.db.models.repay_credit_table import Transaction


@pytest.mark.api
class TestUpUBalance:
    def test_up_u_balance(self, api_manager, create_user_request, up_balance_request, db_session):
        response = api_manager.user_steps.up_balance(
            up_balance_request=up_balance_request,
            user_credentials=create_user_request
        )

        assert response.balance == float(up_balance_request.amount)


        transactions = db_session.query(Transaction).filter(
            Transaction.to_account_id == up_balance_request.accountId,
            Transaction.transaction_type == "deposit"
        ).all()

        assert len(transactions) > 0, "Транзакция пополнения не найдена в БД"

        last_transaction = transactions[-1]
        assert last_transaction.amount == float(up_balance_request.amount), \
            f"Сумма транзакции не совпадает: {last_transaction.amount}"

    def test_get_transactions_after_deposit(self, api_manager, create_user_request, up_balance_request):
        account_id = up_balance_request.accountId
        expected_amount = float(up_balance_request.amount)

        api_manager.user_steps.up_balance(user_credentials=create_user_request, up_balance_request=up_balance_request)

        response = api_manager.user_steps.get_transactions(user_credentials=create_user_request, account_id=account_id)

        assert response.id == account_id
        assert response.balance == expected_amount
        assert len(response.transactions) == 1, "Ожидается ровно одна транзакция"
