from typing import Callable
import pytest
from sqlalchemy.orm import Session
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.get_credit_request import GetCreditRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb


@pytest.mark.api
class TestGetCredit:
    def test_get_credit(
            self,
            api_manager: ApiManager,
            credit_user_credentials: CreateUserRequest,
            get_credit_request: GetCreditRequest,
            db_session: Session
    ):

        response = api_manager.user_steps.get_credit(
            user_request=credit_user_credentials,
            get_credit_request=get_credit_request
        )

        assert response.creditId is not None, "API не вернул ID кредита"

        credit_in_db = CreditCrudDb.get_credit_by_id(db_session, response.creditId)
        assert credit_in_db is not None, f"Кредит id={response.creditId} не найден в БД"

        assert credit_in_db.account_id == get_credit_request.accountId
        assert credit_in_db.amount == pytest.approx(get_credit_request.amount, rel=1e-5)
        assert credit_in_db.term_months == get_credit_request.termMonths

    def test_credit_duplicate_same_account(
            self,
            api_manager: ApiManager,
            credit_user_credentials: CreateUserRequest,
            credit_request_factory: Callable[[int, int | None], GetCreditRequest]
    ):

        account = api_manager.user_steps.create_account(credit_user_credentials)
        api_manager.user_steps.get_credit(credit_user_credentials, credit_request_factory(account.id))

        error_resp = api_manager.user_steps.get_credit(
            credit_user_credentials,
            credit_request_factory(account.id),
            response_spec=ResponseSpecs.request_not_found()  # <-- Исправлено на 404
        )

        assert "Only one active credit allowed per user" in error_resp.get("error", ""), \
            f"Неверное сообщение ошибки: {error_resp}"

    def test_credit_duplicate_different_account(
            self,
            api_manager: ApiManager,
            credit_user_credentials: CreateUserRequest,
            credit_request_factory: Callable[[int, int | None], GetCreditRequest]
    ):

        account1 = api_manager.user_steps.create_account(credit_user_credentials)
        account2 = api_manager.user_steps.create_account(credit_user_credentials)

        api_manager.user_steps.get_credit(credit_user_credentials, credit_request_factory(account1.id))

        error_resp = api_manager.user_steps.get_credit(
            credit_user_credentials,
            credit_request_factory(account2.id),
            response_spec=ResponseSpecs.request_not_found()  # <-- Исправлено на 404
        )

        assert "Only one active credit allowed per user" in error_resp.get("error", ""), \
            f"Неверное сообщение ошибки: {error_resp}"
