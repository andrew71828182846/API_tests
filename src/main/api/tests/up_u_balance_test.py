import requests
import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.up_u_balance_request import UpUBalanceRequest
from src.main.api.models.up_u_balance_response import UpUBalanceResponse


@pytest.mark.api
class Test_up_u_balance:
    def test_up_u_balance(self):
        login_admin_request = LoginUserRequest(username="admin", password="123456")
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_admin_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )
        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get("token")

        create_user_request = CreateUserRequest(username="Max02", password="Pas!sw0rd",role="ROLE_USER")
        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_user_response.status_code == 200

        login_user_request = LoginUserRequest(username="Max02", password="Pas!sw0rd")
        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )
        assert login_user_response.status_code == 200
        token = login_user_response.json().get("token")

        create_accaunt_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_accaunt_response.status_code == 201
        create_account_response_first = CreateAccountResponse(**create_accaunt_response.json())
        assert create_account_response_first.balance == 0

        account_id1 = create_account_response_first.id

        up_u_balance_request = UpUBalanceRequest(accountId=account_id1, amount=1100)
        up_balance_response = requests.post(
            url = "http://localhost:4111/api/account/deposit",
            json = up_u_balance_request.model_dump(),
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
                "accept": "application/json"
            }
        )

        assert up_balance_response.status_code == 200
        up_u_balance_response = UpUBalanceResponse(**up_balance_response.json())
        assert up_u_balance_response.balance == 1100







