import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.get_credit_request import GetCreditRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.transfer_funds_request import TransferFundsRequest
from src.main.api.models.up_u_balance_request import UpUBalanceRequest


@pytest.fixture
def create_user_request(api_manager):
    user_request = CreateUserRequest(username="Max3333", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def up_balance_request(api_manager, create_user_request):
    create_account_response = api_manager.user_steps.create_account(create_user_request)
    return UpUBalanceRequest(
        accountId=create_account_response.id,
        amount=1000
    )

@pytest.fixture
def transfer_test_setup(api_manager):
    sender_request = CreateUserRequest(username="Max322", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(sender_request)
    sender_account = api_manager.user_steps.create_account(sender_request)

    top_up = UpUBalanceRequest(accountId=sender_account.id, amount=2000)
    api_manager.user_steps.up_balance(
        up_balance_request=top_up,
        user_credentials=sender_request
    )

    receiver_request = CreateUserRequest(username="Max228", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(receiver_request)
    receiver_account = api_manager.user_steps.create_account(receiver_request)

    return {
        "sender_creds": sender_request,
        "transfer_request": TransferFundsRequest(
            fromAccountId=sender_account.id,
            toAccountId=receiver_account.id,
            amount=500
        ),
        "expected_sender_balance": 1500
    }



@pytest.fixture
def credit_user_credentials(api_manager):
    user = CreateUserRequest(
        username="Max678",
        password="Pas!sw0rd",
        role="ROLE_CREDIT_SECRET"
    )
    api_manager.admin_steps.create_user(user)
    return user


@pytest.fixture
def get_credit_request(api_manager, credit_user_credentials):
    account = api_manager.user_steps.create_account(credit_user_credentials)

    return GetCreditRequest(
        accountId=account.id,
        amount=5000,
        termMonths=12
    )

@pytest.fixture
def repay_credit_request(api_manager, credit_user_credentials, get_credit_request):
    credit_response = api_manager.user_steps.get_credit(credit_user_credentials, get_credit_request)

    return RepayCreditRequest(
        creditId=credit_response.creditId,
        amount=5000,
        accountId=credit_response.id
    )
