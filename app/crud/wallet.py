import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.base import Wallet


def get_wallet_by_id(db: Session, wallet_id: uuid.UUID):
    stmt = select(Wallet).where(Wallet.id == wallet_id)
    return db.scalar(stmt)

def get_wallet_by_user_id(db: Session, user_id: uuid.UUID):
    stmt = select(Wallet).where(Wallet.user_id == user_id)
    return db.scalar(stmt)