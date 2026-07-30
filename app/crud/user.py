import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.base import User, Wallet
from app.schemas.user import UserCreate


def create_user(db: Session, user: UserCreate):
    user_data = user.model_dump()
    plain_password = user_data.pop("password")
    user_data["hashed_password"] = get_password_hash(plain_password)
    db_user = User(**user_data)
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

def authentic_user(db: Session, email: str, password: str):
    user = db.scalar(select(User).where(User.email == email))
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return user
    return user