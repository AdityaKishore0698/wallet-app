from fastapi import FastAPI

from app.api.routes import auth, transaction, user, wallet
from app.core.database import engine
from app.models.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Digital Wallet API", version="1.0.0")

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(wallet.router)
app.include_router(transaction.router)