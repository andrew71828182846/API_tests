from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime
from src.main.api.db.base import Base


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, autoincrement=True)
    to_account_id = Column(Integer, ForeignKey("account.id"), nullable=True)
    from_account_id = Column(Integer, ForeignKey("account.id"), nullable=True)
    credit_id = Column(Integer, ForeignKey("credit.id"), nullable=True)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Transaction(id={self.id}, type={self.transaction_type}, amount={self.amount})>"