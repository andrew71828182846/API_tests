import pytest

from src.main.api.fixtures.api_fixtures import api_manager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.request.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreateUser():
    def test_create_user_valid(self, api_manager):
        create_user_request = CreateUserRequest(username="Max432", password="Pas!sw0rd",role="ROLE_USER")
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

