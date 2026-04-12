import pytest
from src.main.api.db.crud.credit_crud import CreditCrudDb


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


    def test_credit_only_one_account(self, api_manager, credit_user_credentials, credit_request_factory):
        account1 = api_manager.user_steps.create_account(credit_user_credentials)
        account2 = api_manager.user_steps.create_account(credit_user_credentials)

        api_manager.user_steps.get_credit(credit_user_credentials, credit_request_factory(account1.id))

        expected_error_msg = "Only one active credit allowed per user"

        # ПРОВЕРКА 1: Нельзя взять второй кредит на ТОТ ЖЕ счёт
        with pytest.raises(AssertionError, match=expected_error_msg):
            api_manager.user_steps.get_credit(credit_user_credentials, credit_request_factory(account1.id))

        # ПРОВЕРКА 2: Нельзя взять кредит на ДРУГОЙ счёт
        with pytest.raises(AssertionError, match=expected_error_msg):
            api_manager.user_steps.get_credit(credit_user_credentials, credit_request_factory(account2.id))

