from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.request.delete_all_requester import DeleteAllRequester
from src.main.api.request.login_user_requester import LoginUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestDeleteAll:
    def test_delete_all_test(self):
        login_admin_request = LoginUserRequest(username="admin", password="123456")

        LoginUserRequester(
            request_spec=RequestSpecs.unauth_headers(),
            response_spec=ResponseSpecs.request_ok()
        ).post(login_admin_request)

        DeleteAllRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post()

