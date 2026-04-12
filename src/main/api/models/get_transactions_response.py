from typing import List, Optional
from src.main.api.models.base_model import BaseModel


class TransactionItem(BaseModel):
    transactionId: int
    type: str
    amount: float
    fromAccountId: Optional[int] = None
    toAccountId: Optional[int] = None
    createdAt: str


class TransactionResponse(BaseModel):
    id: int
    number: str
    balance: float
    transactions: List[TransactionItem]