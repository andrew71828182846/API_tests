import requests
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.get_credit_response import GetCreditResponse
from src.main.api.models.get_credit_request import GetCreditRequest
from src.main.api.models.repay_credit_response import RepayCreditResponse
from src.main.api.models.repay_credit_request import RepayCreditRequest



class TestRepayCredit:
    def test_repay_credit(self):
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

        create_user_request = CreateUserRequest(username="Max266", password="Pas!sw0rd",role="ROLE_CREDIT_SECRET")
        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_user_response.status_code == 200

        login_user_request = LoginUserRequest(username="Max266", password="Pas!sw0rd",role="ROLE_CREDIT_SECRET")
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


        accaunt_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert accaunt_response.status_code == 201
        create_accaunt_response = CreateAccountResponse(**accaunt_response.json())
        assert create_accaunt_response.balance == 0

        account_id1 = create_accaunt_response.id

        get_credit_request = GetCreditRequest(accountId=account_id1, amount=5000, termMonths=12)
        credit_response = requests.post(
            url = "http://localhost:4111/api/credit/request",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json = get_credit_request.model_dump()
        )

        assert credit_response.status_code == 201
        get_credit_response = GetCreditResponse(**credit_response.json())


        creditId = get_credit_response.creditId

        repay_credit_request = RepayCreditRequest(creditId=creditId, accountId=account_id1, amount=5000)
        repay_response = requests.post(
            url = "http://localhost:4111/api/credit/repay",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json = repay_credit_request.model_dump()
        )
        assert repay_response.status_code == 200
        repay_credit_response = RepayCreditResponse(**repay_response.json())
        assert repay_credit_response.amountDeposited == repay_credit_request.amount