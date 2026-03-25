import pytest
import requests



@pytest.mark.api
class TestTransferFunds:
    def test_transfer_funds(self):
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
                "username": "Max69",
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
                "username": "Max69",
                "password": "Pas!sw0rd"
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )
        assert login_user_response.status_code == 200
        token = login_user_response.json().get("token")

        create_accaunt_response_first = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_accaunt_response_first.status_code == 201
        assert create_accaunt_response_first.json().get("balance") == 0

        account_id1 = create_accaunt_response_first.json().get("id")


        create_accaunt_response_second = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_accaunt_response_second.status_code == 201
        assert create_accaunt_response_second.json().get("balance") == 0


        account_id2 = create_accaunt_response_second.json().get("id")

        up_u_balance_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": account_id1,
                "amount": 2000
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
                "accept": "application/json"
            }
        )

        assert up_u_balance_response.status_code == 200
        assert up_u_balance_response.json().get("balance") == 2000


        transfer_funds_response = requests.post(
            url="http://localhost:4111/api/account/transfer",
            json={
                "fromAccountId": account_id1,
                "toAccountId": account_id2,
                "amount": 500.75
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
                "accept": "application/json"
            }
        )
        assert transfer_funds_response.status_code == 200