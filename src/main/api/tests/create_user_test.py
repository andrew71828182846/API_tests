import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.request.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreateUser():
    def test_create_user_valid(self):
        create_user_request = CreateUserRequest(username="Max44", password="Pas!sw0rd",role="ROLE_USER")

        response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

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
    def test_create_user_invalid(self, username, password):

        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_bad()
        ).post(create_user_request)

