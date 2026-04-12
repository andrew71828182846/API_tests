import pytest
from sqlalchemy.orm import Session
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.db.crud.user_crud import UserCrudDb
from src.main.api.db.crud.account_crud import AccountCrudDb


@pytest.mark.api
class TestDeleteUser:
    @pytest.mark.parametrize("create_user_request", [RandomModelGenerator.generate(CreateUserRequest)])
    def test_delete_user_soft_delete(self, api_manager: ApiManager, create_user_request, db_session: Session):
        user = api_manager.admin_steps.create_user(create_user_request)
        account = api_manager.user_steps.create_account(create_user_request)

        api_manager.admin_steps.delete_user(user.id)

        user_from_db = UserCrudDb.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.deleted_at is not None, "Пользователь не помечен как удаленный"

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account.id)
        assert account_from_db is not None, "Аккаунт удален вместе с пользователем"