import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.transaction import create_transaction, get_transactions_by_wallet
from app.schemas.transaction import TransactionCreate, TransactionResponse

router = APIRouter(prefix="/transactions", tags=["Transactions"])

db_dependency = Depends(get_db)

@router.post("/{wallet_id}", response_model=TransactionResponse)
def new_transaction(wallet_id: uuid.UUID, transaction_in: TransactionCreate, db: Session = db_dependency):
    try:
        return create_transaction(db, wallet_id, transaction_in)
    except ValueError as e:
        if str(e) == "Wallet not found":
            raise HTTPException(404, detail=str(e))
        if str(e) == "Insufficient funds":
            raise HTTPException(400, detail=str(e))

@router.get("/{wallet_id}/history", response_model=list[TransactionResponse])
def transaction_history(wallet_id: uuid.UUID, db: Session = db_dependency):
    return get_transactions_by_wallet(db, wallet_id)