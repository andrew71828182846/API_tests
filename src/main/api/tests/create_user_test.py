import pytest
from src.main.api.fixtures.api_fixtures import api_manager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateUser():
    @pytest.mark.parametrize("create_user_request", [RandomModelGenerator.generate(CreateUserRequest)])
    def test_create_user_valid(self, api_manager, create_user_request):
        response = api_manager.admin_steps.create_user(create_user_request)


        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

    @pytest.mark.api
    @pytest.mark.parametrize(
        "username,password", [
            ("Мax", "Pas!sw0rd"),
            ("Ma", "Pas!sw0rd"),
            ("MAX!", "Pas!sw0rd"),
            ("Max1", "Pas!sw0rд"),
            ("Max2", "Pas!sw0"),
            ("Max3", "pas!sw0d"),
            ("Max4", "PAS!SWORD"),
            ("Max4", "PASSWORD"),
        ]
    )
    def test_create_user_invalid(self, username, password, api_manager):

        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_invalid_user(create_user_request)

