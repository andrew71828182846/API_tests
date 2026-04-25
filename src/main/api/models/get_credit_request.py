from src.main.api.models.base_model import BaseModel



class GetCreditRequest(BaseModel):
    accountId: int
    amount: float
    termMonths: int