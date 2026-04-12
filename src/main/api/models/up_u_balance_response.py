from src.main.api.models.base_model import BaseModel


class UpUBalanceResponse(BaseModel):
    id: int
    balance: float