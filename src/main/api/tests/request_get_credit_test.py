import pytest

from main.api.db.crud.credit_crud import CreditCrudDb


@pytest.mark.api
class TestGetCredit:
    def test_get_credit(self, api_manager, credit_user_credentials, get_credit_request, db_session):
        response = api_manager.user_steps.get_credit(
            user_request=credit_user_credentials,
            get_credit_request=get_credit_request
        )
        assert response.creditId is not None

        credit_in_db = CreditCrudDb.get_credit_by_id(db_session, response.creditId)

        assert credit_in_db is not None, f"Кредит с id={response.creditId} не найден в БД"
        assert credit_in_db.account_id == get_credit_request.accountId, "credit.account_id не совпадает"
        assert credit_in_db.amount == get_credit_request.amount, "credit.amount не совпадает"
        assert credit_in_db.term_months == get_credit_request.termMonths, "credit.term_months не совпадает"