from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.user import create_user
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/user", tags=["Users"])

db_dependency = Depends(get_db)

@router.post("/", response_model=UserResponse)
def fun(user_in: UserCreate, db: Session = db_dependency):
    try:
        return create_user(db, user_in)
    except IntegrityError:
        raise HTTPException(400, detail="Email already registered")