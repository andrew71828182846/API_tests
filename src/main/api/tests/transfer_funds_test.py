import pytest
import requests
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.transfer_funds_request import TransferFundsRequest
from src.main.api.models.up_u_balance_request import UpUBalanceRequest
from src.main.api.models.up_u_balance_response import UpUBalanceResponse


@pytest.mark.api
class TestTransferFunds:
    def test_transfer_funds(self):
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

        create_user_request = CreateUserRequest(username="Max69", password="Pas!sw0rd",role="ROLE_USER")
        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_user_response.status_code == 200

        login_user_request = LoginUserRequest(username="Max69", password="Pas!sw0rd")
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


        create_account_response_first1 = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_account_response_first1.status_code == 201
        create_account_response_first = CreateAccountResponse(**create_account_response_first1.json())
        assert create_account_response_first.balance == 0

        account_id1 = create_account_response_first.id


        create_accaunt_response_second2 = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_accaunt_response_second2.status_code == 201
        create_account_response_second = CreateAccountResponse(**create_accaunt_response_second2.json())
        assert create_account_response_second.balance == 0

        account_id2 = create_account_response_second.id

        up_u_balance_request = UpUBalanceRequest(accountId=account_id1,amount=2000 )
        up_balance_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json=up_u_balance_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
                "accept": "application/json"
            }
        )

        assert up_balance_response.status_code == 200
        up_u_balance_response = UpUBalanceResponse(**up_balance_response.json())
        assert up_u_balance_response.balance == 2000

        transfer_funds_request = TransferFundsRequest(fromAccountId=account_id1, toAccountId=account_id2, amount=500.75)
        transfer_funds_response = requests.post(
            url="http://localhost:4111/api/account/transfer",
            json=transfer_funds_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
                "accept": "application/json"
            }
        )
        assert transfer_funds_response.status_code == 200