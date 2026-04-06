from typing import Optional, Type
from dataclasses import dataclass
from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from enum import Enum

from src.main.api.models.get_credit_request import GetCreditRequest
from src.main.api.models.get_credit_response import GetCreditResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.repay_credit_response import RepayCreditResponse
from src.main.api.models.transfer_funds_request import TransferFundsRequest
from src.main.api.models.transfer_funds_response import TransferFundsResponse
from src.main.api.models.up_u_balance_request import UpUBalanceRequest
from src.main.api.models.up_u_balance_response import UpUBalanceResponse


@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        url="/admin/create",
        request_model=CreateUserRequest,
        response_model=CreateUserResponse
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        url="/admin/users",
        request_model=None,
        response_model=None
    )

    LOGIN_USER = EndpointConfiguration(
        request_model=LoginUserRequest,
        url="/auth/token/login",
        response_model=LoginUserResponse
    )

    CREATE_ACCOUNT = EndpointConfiguration(
        request_model=None,
        url="/account/create",
        response_model=CreateAccountResponse
    )

    UP_BALANCE = EndpointConfiguration(
        request_model=UpUBalanceRequest,
        url="/account/deposit",
        response_model=UpUBalanceResponse
    )

    TRANSFER_FUNDS = EndpointConfiguration(
        request_model=TransferFundsRequest,
        url="/account/transfer",
        response_model=TransferFundsResponse
    )

    GET_CREDIT = EndpointConfiguration(
        request_model=GetCreditRequest,
        url="/credit/request",
        response_model=GetCreditResponse
    )

    REPAY_CREDIT = EndpointConfiguration(
        request_model=RepayCreditRequest,
        url="/credit/repay",
        response_model=RepayCreditResponse
    )