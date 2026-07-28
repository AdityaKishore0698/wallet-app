import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.user import create_user, get_user_by_id
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

db_dependency = Depends(get_db)

@router.post("/", response_model=UserResponse)
def register_user(user_in: UserCreate, db: Session = db_dependency):
    try:
        return create_user(db, user_in)
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, detail="Email already registered")

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: uuid.UUID, db: Session = db_dependency):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, detail="User not found")
    return user
        
