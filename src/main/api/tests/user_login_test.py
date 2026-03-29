import pytest
import requests

from src.main.api.models import login_user_request
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


@pytest.mark.api
class TestLoginUser:
    def test_login_admin(self):
        login_admin_request = LoginUserRequest(username="admin", password="123456")
        admin_response = requests.post(
            url = "http://localhost:4111/api/auth/token/login",
            json = login_admin_request.model_dump(),
            headers = {
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )
        assert admin_response.status_code == 200
        login_admin_response = LoginUserResponse(**admin_response.json())
        assert login_admin_response.user.username == login_admin_request.username

        token = login_admin_response.token

        create_user_request = CreateUserRequest(username="Max77", password="Pas!sw0rd", role="ROLE_USER")
        create_user_response = requests.post(
            url = "http://localhost:4111/api/admin/create",
            json = create_user_request.model_dump(),
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_user_response.status_code == 200

        login_user_request = LoginUserRequest(username="Max77", password="Pas!sw0rd")
        user_response = requests.post(
            url = "http://localhost:4111/api/auth/token/login",
            json = login_user_request.model_dump(),
            headers = {
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )
        assert user_response.status_code == 200
        login_user_response = LoginUserResponse(**user_response.json())
        assert login_user_response.user.username == login_user_request.username