from http.client import responses

from requests import post
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.get_credit_request import GetCreditRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.transfer_funds_request import TransferFundsRequest
from src.main.api.models.up_u_balance_request import UpUBalanceRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def up_balance(self, user_credentials: CreateUserRequest, up_balance_request: UpUBalanceRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=user_credentials.username, password=user_credentials.password),
            Endpoint.UP_BALANCE,
            ResponseSpecs.request_ok()
        ).post(up_balance_request)
        return response

    def transfer_funds(self, transfer_funds_request: TransferFundsRequest, user_credentials: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=user_credentials.username, password=user_credentials.password),
            Endpoint.TRANSFER_FUNDS,
            ResponseSpecs.request_ok()
        ).post(transfer_funds_request)
        return response

    def get_credit(self, user_request, get_credit_request: GetCreditRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=user_request.username, password=user_request.password),
            Endpoint.GET_CREDIT,
            ResponseSpecs.request_created()
        ).post(get_credit_request)
        return response

    def repay_credit(self, user_credentials: CreateUserRequest, repay_credit_request: RepayCreditRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=user_credentials.username, password=user_credentials.password),
            Endpoint.REPAY_CREDIT,
            ResponseSpecs.request_ok()
        ).post(repay_credit_request)
        return response