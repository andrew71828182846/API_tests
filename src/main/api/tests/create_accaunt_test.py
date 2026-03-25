import requests
import pytest

@pytest.mark.api
class TestCreateAccaunt:
    def test_create_accaunt(self):
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )
        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get("token")

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Max55",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_user_response.status_code == 200

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Max55",
                "password": "Pas!sw0rd"
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )
        assert login_user_response.status_code == 200
        token = login_user_response.json().get("token")

        create_accaunt_response = requests.post(
            url = "http://localhost:4111/api/account/create",
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_accaunt_response.status_code == 201
        assert create_accaunt_response.json().get("balance") == 0
