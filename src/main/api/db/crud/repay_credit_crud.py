from sqlalchemy.orm import Session
from sqlalchemy import desc
from src.main.api.db.models.repay_credit_table import Transaction


class TransactionCrudDb:
    @staticmethod
    def get_transactions_by_credit(db: Session, credit_id: int) -> list[type[Transaction]]:
        return db.query(Transaction).filter(Transaction.credit_id == credit_id).order_by(desc(Transaction.created_at)).all()