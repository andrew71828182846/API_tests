
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime
from src.main.api.db.base import Base


class Credit(Base):
    __tablename__ = "credit"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    amount = Column(Float, nullable=False)
    term_months = Column(Integer, nullable=False)
    balance = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime, nullable=False)

    def __repr__(self) -> str:
        return f"<Credit(id={self.id}, account_id={self.account_id}, balance={self.balance}, term={self.term_months}m)>"