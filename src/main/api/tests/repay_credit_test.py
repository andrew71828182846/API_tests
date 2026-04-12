
from main.api.db.crud.credit_crud import CreditCrudDb
from main.api.db.crud.repay_credit_crud import TransactionCrudDb
from src.main.api.models.repay_credit_request import RepayCreditRequest



class TestRepayCredit:
    def test_repay_credit(self, api_manager, repay_credit_request: RepayCreditRequest, credit_user_credentials, db_session):
        response = api_manager.user_steps.repay_credit(credit_user_credentials, repay_credit_request)

        assert response.amountDeposited == repay_credit_request.amount


        transactions = TransactionCrudDb.get_transactions_by_credit(db_session, repay_credit_request.creditId)
        assert len(transactions) > 0, "Транзакции по погашению кредита не найдены в БД"

        last_transaction = transactions[0]
        assert last_transaction.amount == repay_credit_request.amount, "Сумма транзакции не совпадает"
        assert last_transaction.credit_id == repay_credit_request.creditId, "transaction.credit_id не совпадает"
        assert last_transaction.from_account_id == repay_credit_request.accountId, "transaction.from_account_id не совпадает"


        credit_in_db = CreditCrudDb.get_credit_by_id(db_session, repay_credit_request.creditId)
        assert credit_in_db is not None, "Кредит не найден в БД"

