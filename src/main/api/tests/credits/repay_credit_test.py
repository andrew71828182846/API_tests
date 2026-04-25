import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.models.repay_credit_request import RepayCreditRequest


class TestRepayCredit:
    def test_repay_credit(
            self,
            api_manager: ApiManager,
            repay_credit_request: RepayCreditRequest,
            credit_user_credentials: CreateUserRequest,
            db_session: Session
    ):

        credit_before = CreditCrudDb.get_credit_by_id(db_session, repay_credit_request.creditId)
        assert credit_before is not None, "Кредит не найден"
        initial_balance = credit_before.balance

        response = api_manager.user_steps.repay_credit(
            credit_user_credentials,
            repay_credit_request
        )

        db_session.expire_all()

        assert response.amountDeposited == pytest.approx(repay_credit_request.amount, rel=1e-5)

        credit_after = CreditCrudDb.get_credit_by_id(db_session, repay_credit_request.creditId)
        assert credit_after is not None, "Кредит исчез после погашения"
        expected_balance = initial_balance + repay_credit_request.amount

        assert credit_after.balance == pytest.approx(expected_balance, rel=1e-5), \
            f"Баланс не обновился. Было: {initial_balance}, Ожидалось: {expected_balance}, Факт: {credit_after.balance}"
        assert credit_after.amount == credit_before.amount
        assert credit_after.created_at == credit_before.created_at


