import pytest
from sqlalchemy.orm import Session

from src.main.api.db.crud.user_crud import UserCrudDb
from src.main.api.fixtures.api_fixtures import ApiManager
from src.main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestLoginUser:
    def test_login_admin(self, api_manager, db_session):
        login_admin_request = LoginUserRequest(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(login_admin_request)


        assert login_admin_request.username == response.user.username
        assert response.user.role == "ROLE_ADMIN"

        user_from_db = UserCrudDb.get_user_by_username(db_session, login_admin_request.username)
        assert user_from_db is not None, "Пользователь admin не найден в БД"
        assert user_from_db.role == "ROLE_ADMIN", "Роль admin в БД не совпадает"
        assert user_from_db.deleted_at is None, "Пользователь admin удален"

    def test_login_user(self, api_manager, create_user_request, db_session):
        response = api_manager.admin_steps.login_user(create_user_request)

        assert create_user_request.username == response.user.username
        assert response.user.role == "ROLE_USER"

        user_from_db = UserCrudDb.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is not None, f"Пользователь {create_user_request.username} не найден в БД"
        assert user_from_db.role == create_user_request.role, "Роль пользователя в БД не совпадает"
        assert user_from_db.deleted_at is None, f"Пользователь {create_user_request.username} удален"


    def test_get_all_users_db_sync(self, api_manager: ApiManager, user_data, db_session: Session):
        api_manager.admin_steps.create_user(user_data)

        api_manager.admin_steps.get_all_users()

        user_from_db = UserCrudDb.get_user_by_username(db_session, user_data.username)
        assert user_from_db is not None, "Пользователь не создан в БД"
        assert user_from_db.deleted_at is None, "Пользователь помечен как удаленный"
