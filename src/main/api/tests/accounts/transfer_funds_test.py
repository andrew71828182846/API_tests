from typing import Any

import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb


@pytest.mark.api
class TestTransferFunds:
    def test_transfer_funds(self, api_manager: ApiManager, transfer_funds_request: dict[str, Any], db_session: Session):
        response = api_manager.user_steps.transfer_funds(
            transfer_funds_request=transfer_funds_request["transfer_request"],
            user_credentials=transfer_funds_request["sender_creds"]
        )

        assert response.fromAccountIdBalance == float(transfer_funds_request["expected_sender_balance"])

        sender_account_db = AccountCrudDb.get_account_by_id(
            db_session,
            transfer_funds_request["sender_account"].id
        )
        assert sender_account_db.balance == response.fromAccountIdBalance, \
            "Баланс отправителя в БД не совпадает с API"


