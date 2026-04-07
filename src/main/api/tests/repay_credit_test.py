
from src.main.api.models.repay_credit_request import RepayCreditRequest



class TestRepayCredit:
    def test_repay_credit(self, api_manager, repay_credit_request: RepayCreditRequest, credit_user_credentials):
        response = api_manager.user_steps.repay_credit(credit_user_credentials, repay_credit_request)

        assert response.amountDeposited == repay_credit_request.amount