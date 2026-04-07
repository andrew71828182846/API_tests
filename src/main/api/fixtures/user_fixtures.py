import random

import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.get_credit_request import GetCreditRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.transfer_funds_request import TransferFundsRequest
from src.main.api.models.up_u_balance_request import UpUBalanceRequest


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def up_balance_request(api_manager, create_user_request):
    create_account_response = api_manager.user_steps.create_account(create_user_request)
    amount = random.randint(1000, 9000)
    return UpUBalanceRequest(
        accountId=create_account_response.id,
        amount=amount
    )


@pytest.fixture
def transfer_funds_request(api_manager, create_user_request):
    sender_account = api_manager.user_steps.create_account(create_user_request)


    transfer_amount = random.randint(500, 2000)


    deposit_amount = transfer_amount + 1000
    top_up = UpUBalanceRequest(accountId=sender_account.id, amount=deposit_amount)
    api_manager.user_steps.up_balance(
        up_balance_request=top_up,
        user_credentials=create_user_request
    )

    receiver_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(receiver_request)
    receiver_account = api_manager.user_steps.create_account(receiver_request)

    return {
        "sender_creds": create_user_request,
        "sender_account": sender_account,
        "receiver_account": receiver_account,
        "transfer_request": TransferFundsRequest(
            fromAccountId=sender_account.id,
            toAccountId=receiver_account.id,
            amount=transfer_amount
        ),
        "expected_sender_balance": deposit_amount - transfer_amount
    }

@pytest.fixture
def credit_user_credentials(api_manager):
    user = RandomModelGenerator.generate(CreateUserRequest)
    user.role = "ROLE_CREDIT_SECRET"
    api_manager.admin_steps.create_user(user)
    return user

@pytest.fixture
def get_credit_request(api_manager, credit_user_credentials):
    account = api_manager.user_steps.create_account(credit_user_credentials)
    amount = random.randint(5000, 15000)
    return GetCreditRequest(
        accountId=account.id,
        amount=amount,
        termMonths=12
    )

@pytest.fixture
def repay_credit_request(api_manager, credit_user_credentials, get_credit_request):
    credit_response = api_manager.user_steps.get_credit(credit_user_credentials, get_credit_request)

    return RepayCreditRequest(
        creditId=credit_response.creditId,
        amount=get_credit_request.amount,
        accountId=get_credit_request.accountId
    )
