from src.main.api.models.base_model import BaseModel


class UpUBalanceRequest(BaseModel):
    accountId: int
    amount: float