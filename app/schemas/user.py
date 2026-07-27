import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str | None = None

class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    first_name: str
    last_name: str | None = None
    wallet_id: uuid.UUID | None = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)