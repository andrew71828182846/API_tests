import requests
import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestCreateUser():
    def test_create_user_valid(self):
        login_user_request = LoginUserRequest(username="admin", password="123456")
        login_admin_response = requests.post(
            url = "http://localhost:4111/api/auth/token/login",
            json = login_user_request.model_dump(),
            headers = {
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )
        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get("token")

        create_user_request = CreateUserRequest(username="Max44", password="Pas!sw0rd",role="ROLE_USER")
        user_response = requests.post(
            url = "http://localhost:4111/api/admin/create",
            json = create_user_request.model_dump(),
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert user_response.status_code == 200
        create_user_response = CreateUserResponse(**user_response.json())
        assert create_user_response.username == create_user_request.username
        assert create_user_response.role == create_user_request.role

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
        login_user_request = LoginUserRequest(username="admin", password="123456")
        login_admin_response = requests.post(
            url = "http://localhost:4111/api/auth/token/login",
            json = login_user_request.model_dump(),
            headers = {
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )
        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get("token")

        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        create_user_response = requests.post(
            url = "http://localhost:4111/api/admin/create",
            json = create_user_request.model_dump(),
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_user_response.status_code == 400