import pytest
import requests


class TestRepayCredit:
    def test_repay_credit(self):
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
                "username": "Max123",
                "password": "Pas!sw0rd",
                "role": "ROLE_CREDIT_SECRET"
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
                "username": "Max123",
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
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_accaunt_response.status_code == 201
        assert create_accaunt_response.json().get("balance") == 0

        account_id1 = create_accaunt_response.json().get("id")

        get_credit_response = requests.post(
            url = "http://localhost:4111/api/credit/request",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json = {
                "accountId": account_id1,
                "amount": 5000,
                "termMonths": 12
            }
        )

        assert get_credit_response.status_code == 201
        assert get_credit_response.json().get("balance") == 5000

        creditId = get_credit_response.json().get("creditId")


        repay_credit_response = requests.post(
            url = "http://localhost:4111/api/credit/repay",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json = {
                "creditId": creditId,
                "accountId": account_id1,
                "amount": 5000
            }
        )
        assert repay_credit_response.status_code == 200
