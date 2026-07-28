import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.wallet import get_wallet_by_user_id
from app.schemas.wallet import WalletResponse

router = APIRouter(prefix="/wallets", tags=["Wallets"])

db_dependency = Depends(get_db)

@router.get("/user/{user_id}", response_model=WalletResponse)
def get_wallet(user_id: uuid.UUID, db: Session = db_dependency):
    wallet = get_wallet_by_user_id(db, user_id)
    if not wallet:
        raise HTTPException(404, detail="Wallet not found")
    return wallet