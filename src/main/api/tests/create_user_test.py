import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.api_fixtures import api_manager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User
from sqlalchemy.orm import Session

@pytest.mark.api
class TestCreateUser():
    @pytest.mark.parametrize("create_user_request", [RandomModelGenerator.generate(CreateUserRequest)])
    def test_create_user_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.admin_steps.create_user(create_user_request)


        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username, 'Созданного пользователя нет в БД'


    @pytest.mark.api
    @pytest.mark.parametrize(
        "username,password", [
            ("Мax", "Pas!sw0rd"),
            ("Ma", "Pas!sw0rd"),
            ("MAX!", "Pas!sw0rd"),
            ("Maxx1", "Pas!sw0rде"),
            ("Maxx2", "Pas!sw0"),
            ("Maxx3", "pas!sw0d"),
            ("Maxx4", "PAS!SWORD"),
            ("Maxx4", "PASSWORD"),
        ]
    )
    def test_create_user_invalid(self, db_session: Session, username: str, password: str, api_manager: ApiManager):

        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        print(f"🚀 PAYLOAD: {create_user_request.model_dump()}")
        api_manager.admin_steps.create_invalid_user(create_user_request)


        user_from_db = User.get_user_by_username(db_session, create_user_request.username)

        assert user_from_db is None, 'Пользователь создан, ошибка'
