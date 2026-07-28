import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.base import User, Wallet
from app.schemas.user import UserCreate


def create_user(db: Session, user: UserCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.flush()
    new_wallet = Wallet(user_id=db_user.id, balance=0, currency="INR")
    db.add(new_wallet)
    db.commit()
    db.refresh(db_user)
    db_user.wallet_id = new_wallet.id
    return db_user

def get_user_by_id(db: Session, user_id: uuid.UUID):
    stmt = select(User).where(User.id == user_id)
    return db.scalar(stmt)